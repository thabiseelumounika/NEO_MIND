import sqlite3
import os

db_path = os.path.join('database', 'users.db')
print(f"Checking database at: {os.path.abspath(db_path)}")

if not os.path.exists(db_path):
    print("❌ Database file does not exist!")
else:
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    result = c.fetchone()
    if result:
        print("✅ 'users' table exists.")
        c.execute("SELECT COUNT(*) FROM users;")
        count = c.fetchone()[0]
        print(f"📊 Number of users: {count}")
    else:
        print("❌ 'users' table does NOT exist.")
    conn.close()
