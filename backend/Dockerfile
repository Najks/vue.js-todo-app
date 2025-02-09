# Uporabi uradno Python sliko
FROM python:3.10

# Nastavi delovni imenik
WORKDIR /app

# Kopiraj datoteke v kontejner
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj kodo aplikacije
COPY . .

# Zaženi Flask aplikacijo
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
