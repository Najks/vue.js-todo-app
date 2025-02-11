FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

RUN mkdir -p /data && chmod 777 /data

ENV DATABASE_PATH=/app/database.db

CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
