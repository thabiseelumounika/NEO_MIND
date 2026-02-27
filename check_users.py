import sqlite3
import os

# Ensure 'database' directory exists
os.makedirs('database', exist_ok=True)
DB_PATH = os.path.join('database', 'users.db')

# Connect & fetch data
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("SELECT * FROM users")
users = c.fetchall()
conn.close()

if users:
    print("Users in database:")
    for user in users:
        print(user)
else:
    print("No users found.")

