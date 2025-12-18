# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Copy frontend files (HTML, CSS, JS)
COPY frontend ./frontend

# Install sqlite3 and curl
RUN apt-get update && apt-get install -y sqlite3 curl && rm -rf /var/lib/apt/lists/*

# Create data directory for SQLite DB
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=development

# Set the entrypoint
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
