import sqlite3
import os

# Ensure the database directory exists
os.makedirs('database', exist_ok=True)

DB_PATH = os.path.join('database', 'users.db')

# Connect to the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create the users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert a test user
c.execute("DELETE FROM users")  # Optional: clear old data
c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
          ('Mounika', 'thabiseelumounika@gmail.com', '123456'))
          
conn.commit()
conn.close()

print("✅ Database created and test user inserted.")


