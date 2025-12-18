FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y sqlite3 curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY backend ./backend
COPY frontend ./frontend

RUN mkdir -p /app/data
EXPOSE 5000
CMD ["python", "backend/app.py"]
