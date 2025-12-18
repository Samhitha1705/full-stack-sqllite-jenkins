# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and frontend
COPY backend ./backend
COPY frontend ./frontend

# Install sqlite3 and curl
RUN apt-get update && apt-get install -y sqlite3 curl && rm -rf /var/lib/apt/lists/*

# Create data folder
RUN mkdir -p /app/data

# Set environment variables for Flask
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=development

# Expose port
EXPOSE 5000

# Run Flask on all interfaces
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
