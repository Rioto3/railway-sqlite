import sqlite3
import os

DATABASE_PATH = "/data/main.db"

def init_database():
    # Ensure data directory exists
    os.makedirs("/data", exist_ok=True)
    
    # Create database and sample tables
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create sample tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Insert sample data
    cursor.execute('''
        INSERT OR IGNORE INTO users (name, email) VALUES 
        ('Alice', 'alice@example.com'),
        ('Bob', 'bob@example.com'),
        ('Charlie', 'charlie@example.com')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO posts (user_id, title, content) VALUES 
        (1, 'Hello World', 'This is my first post'),
        (1, 'SQLite is Great', 'I love working with SQLite'),
        (2, 'Railway Deployment', 'Deploying on Railway is easy'),
        (3, 'FastAPI Tutorial', 'Building APIs with FastAPI')
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

if __name__ == "__main__":
    init_database()