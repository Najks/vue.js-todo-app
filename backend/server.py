import os
import random
import string
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date, timedelta
from datetime import datetime


# 📌 KONFIGURACIJA APLIKACIJE
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.getenv("DATABASE_PATH", os.path.join(os.path.dirname(__file__), "database.db"))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})  # 🔹 Omejen CORS
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String(50), primary_key=True)  
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.String(50), db.ForeignKey("user.id"))
    date = db.Column(db.Date, nullable=False, default=date.today)
    

# 📌 USTVARJANJE BAZE
with app.app_context():
    if not os.path.exists(DATABASE_PATH):
        db.create_all()
        print("📌 SQLite baza podatkov je bila ustvarjena.")

# 📌 GENERIRANJE RANDOM UPORABNIŠKEGA ID
def generate_user_id():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))

# 📌 API: REGISTRACIJA
@app.route("/auth/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    new_user = User(id=generate_user_id(), username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Uporabnik ustvarjen!", "user_id": new_user.id}), 201

# 📌 API: PRIJAVA
@app.route("/auth/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        return jsonify({"user_id": user.id, "username": user.username})  
    return jsonify({"message": "Nepravilen username ali geslo"}), 401

@app.route("/api/users/stats", methods=["GET"])
def get_user_stats():
    user_id = request.args.get("user_id")

    if not user_id:
        return jsonify({"message": "User ID je potreben!"}), 400
    
    completed_count = Todo.query.filter_by(user_id=user_id, done=True).count()
    pending_count = Todo.query.filter_by(user_id=user_id, done=False).count()

    frequent_tasks =(
        db.session.query(Todo.task, db.func.count(Todo.task).label("count"))
        .filter_by(user_id=user_id)
        .group_by(Todo.task)
        .order_by(db.desc("count"))
        .limit(5)
        .all()
    )

    frequent_tasks_list = [{"task": t[0], "count": t[1]} for t in frequent_tasks]

    last_7_days = date.today() - timedelta(days=7)
    weekly_tasks = (
        db.session.query(Todo.task.db.func.count(Todo.id).label("count"))
        .filter(Todo.user_id == user_id, Todo.date >= last_7_days)
        .group_by(Todo.date)
        .order_by(Todo.date)
        .all()
    )

    weekly_tasks = [{"date": str(t[0]), "count": t[1]} for t in weekly_tasks]
    return jsonify({
        "completed": completed_count,
        "pending": pending_count,
        "frequent_tasks": frequent_tasks_list,
        "weekly_tasks": weekly_tasks
    })


# 📌 API: PRIDOBI OPRAVILA
@app.route("/api/todos", methods=["GET"])
def get_todos():
    user_id = request.args.get("user_id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    if not user_id:
        return jsonify({"message": "User ID je potreben!"}), 400

    query = Todo.query.filter_by(user_id=user_id)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            query = query.filter(Todo.date >= start_date)  # 🔹 Filtrira opravila od začetnega datuma
        except ValueError:
            return jsonify({"message": "Neveljaven format začetnega datuma!"}), 400

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            query = query.filter(Todo.date <= end_date)  # 🔹 Filtrira opravila do končnega datuma
        except ValueError:
            return jsonify({"message": "Neveljaven format končnega datuma!"}), 400

    todos = query.all()
    return jsonify([{
        "id": t.id,
        "task": t.task,
        "done": t.done,
        "date": str(t.date)
    } for t in todos])

# 📌 API: FILTRIRANJE OPRAVIL
@app.route("/api/todos/filter", methods=["GET"])
def filter_todos():
    user_id = request.args.get("user_id")
    status = request.args.get("status")  # Možne vrednosti: "all", "done", "undone"

    if not user_id:
        return jsonify({"message": "User ID je potreben!"}), 400

    query = Todo.query.filter_by(user_id=user_id)

    if status == "done":
        query = query.filter_by(done=True)
    elif status == "undone":
        query = query.filter_by(done=False)

    todos = query.all()
    return jsonify([{"id": t.id, "task": t.task, "done": t.done} for t in todos])

# 📌 API: DODAJ OPRAVILO
@app.route("/api/todos", methods=["POST"])
def add_todo():
    data = request.json
    user_id = data.get("user_id")  
    task_text = data.get("task", "").strip()

    # 🔹 PREVERI, ALI JE DATUM POSLAN
    if "date" in data:
        try:
            task_date = datetime.strptime(data["date"], "%Y-%m-%d").date()  # ✅ Pretvori `str` v `date`
        except ValueError:
            return jsonify({"message": "Neveljaven format datuma!"}), 400
    else:
        task_date = date.today()  # ✅ Če ni poslan, uporabi današnji datum

    if not user_id or not task_text:
        return jsonify({"message": "Napaka v podatkih!"}), 400

    new_todo = Todo(task=task_text, done=data.get("done", False), user_id=user_id, date=task_date)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({
        "id": new_todo.id,
        "task": new_todo.task,
        "done": new_todo.done,
        "date": str(new_todo.date),  # ✅ Vrni datum kot string
        "message": "Opravilo uspešno dodano!"
    }), 201


# 📌 API: POSODOBI OPRAVILO (BESEDILO ALI STATUS)
@app.route("/api/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json
    todo = Todo.query.get(todo_id)

    if not todo:
        return jsonify({"message": "Opravilo ne obstaja!"}), 404

    todo.task = data.get("task", todo.task)
    todo.done = data.get("done", todo.done)

    if "date" in data:
        try:
            todo.date = datetime.strptime(data["date"], "%Y-%m-%d").date()  # 🔹 Posodobi datum opravila
        except ValueError:
            return jsonify({"message": "Neveljaven format datuma!"}), 400

    db.session.commit()
    return jsonify({
        "message": "Opravilo posodobljeno!",
        "task": todo.task,
        "done": todo.done,
        "date": str(todo.date)
    })

# 📌 API: IZBRIŠI OPRAVILO
@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if not todo:
        return jsonify({"message": "Opravilo ne obstaja!"}), 404

    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Opravilo izbrisano!"})

@app.route("/")
def home():
    return "📦 Flask API"

# 📌 ZAGON STREŽNIKA
if __name__ == "__main__":
    print("📌 Flask backend je zagnan in posluša zahteve...")
    app.run(host="0.0.0.0", port=5000, debug=True)
