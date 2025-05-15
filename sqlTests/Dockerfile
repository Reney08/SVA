FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libmariadb-dev gcc && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set working directory to where app.py is
WORKDIR /app/SQL

EXPOSE 5000

CMD ["python", "app.py"]
