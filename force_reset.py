import sqlite3
import os
from werkzeug.security import generate_password_hash

# Delete old database
if os.path.exists("database.db"):
    os.remove("database.db")
    print("✅ Old database deleted")

# Create new database
conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Create users table
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)
""")

# Add users
cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
           ('admin', generate_password_hash('1234'), 'admin'))
cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
           ('teacher', generate_password_hash('1234'), 'teacher'))

conn.commit()
conn.close()

print("\n✅ Fresh database created!")
print("="*40)
print("Admin Login: admin / 1234")
print("Teacher Login: teacher / 1234")
print("="*40)