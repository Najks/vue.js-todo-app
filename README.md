# 📝 TODO Flask + Vue Aplikacija

To je preprosta **TODO aplikacija**, ki uporablja **Flask (Python) za backend** in **Vue.js (Vue CLI) za frontend**. Aplikacija omogoča **registracijo, prijavo, dodajanje, urejanje in brisanje opravil**.

## 🚀 Zagon aplikacije z Dockerjem

1. **Kloniraj repozitorij**  
   ```sh
   git clone https://github.com/tvoj-github/todo-flask-vue.git
   cd todo-flask-vue
   ```

2. **Zaženi Docker konteinerja**  
   ```sh
   docker compose up --build
   ```

3. **Dostop do aplikacije**  
   - Backend bo na voljo na: `http://localhost:5000`
   - Frontend bo na voljo na: `http://localhost:8080`

## 🔧 Ročni zagon aplikacije (brez Dockerja)

1. **Namestitev backend odvisnosti**  
   ```sh
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python server.py
   ```

2. **Namestitev frontend odvisnosti in zagon**  
   ```sh
   cd ../frontend
   npm install
   npm run serve
   ```

## 📂 Struktura projekta
```
TODO-flask-vue/
│── backend/  # Flask backend
│   ├── server.py  # Glavna aplikacija
│   ├── database.db  # SQLite baza
│   ├── requirements.txt  # Odvisnosti
│   ├── Dockerfile  # Docker konfiguracija
│── frontend/  # Vue.js frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vue.config.js
│   ├── Dockerfile  # Docker konfiguracija
│── docker-compose.yml  # Docker Compose konfiguracija
```

## 🛠 API Končne točke

- **POST** `/auth/register` – Registracija uporabnika
- **POST** `/auth/login` – Prijava uporabnika
- **GET** `/api/todos` – Pridobi opravila
- **POST** `/api/todos` – Dodaj opravilo
- **PUT** `/api/todos/<id>` – Posodobi opravilo
- **DELETE** `/api/todos/<id>` – Izbriši opravilo

## 🔗 Tehnologije

- **Backend:** Python, Flask, SQLAlchemy, Gunicorn
- **Frontend:** Vue.js (Vue CLI), Axios
- **Baza podatkov:** SQLite
- **Docker:** Docker & Docker Compose
- **Proxy:** Nginx


## 🏁 Zaključek

Ta aplikacija omogoča enostavno upravljanje opravil, pri čemer uporablja sodobne tehnologije in je enostavno razširljiva. 
