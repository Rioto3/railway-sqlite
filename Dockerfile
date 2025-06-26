FROM python:3.11-slim

WORKDIR /app

# Install SQLite and dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY app.py .
COPY init_db.py .

# Create volume mount point for persistent data
RUN mkdir -p /data

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]