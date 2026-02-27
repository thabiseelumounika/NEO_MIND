# init_db.py

import sqlite3
import os

# Make sure the database folder exists
os.makedirs('database', exist_ok=True)

# Path to the database
DB_PATH = os.path.join('database', 'users.db')

# Connect to the database (will create if not exists)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create the users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ users.db created with 'users' table.")
