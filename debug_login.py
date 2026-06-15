import sqlite3
from werkzeug.security import check_password_hash

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Check if users table exists
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
if not cur.fetchone():
    print("❌ Users table does NOT exist!")
    print("Creating users table...")
    cur.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)
    conn.commit()
    print("✅ Users table created!")

# Check all users
cur.execute("SELECT id, username, password, role FROM users")
users = cur.fetchall()

print("\n" + "="*50)
print("Current Users in Database:")
print("="*50)

if len(users) == 0:
    print("⚠️ No users found in database!")
    print("\nAdding default users...")
    
    from werkzeug.security import generate_password_hash
    
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
               ('admin', generate_password_hash('1234'), 'admin'))
    cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
               ('teacher', generate_password_hash('1234'), 'teacher'))
    conn.commit()
    
    print("✅ Default users added!")
    print("   Admin: admin / 1234")
    print("   Teacher: teacher / 1234")
    
    # Fetch again
    cur.execute("SELECT id, username, password, role FROM users")
    users = cur.fetchall()

for user in users:
    print(f"ID: {user[0]}")
    print(f"Username: {user[1]}")
    print(f"Password Hash: {user[2][:50]}...")
    print(f"Role: {user[3]}")
    
    # Check if password is 1234
    if check_password_hash(user[2], '1234'):
        print(f"✅ Password for '{user[1]}' is 1234 (CORRECT)")
    else:
        print(f"❌ Password for '{user[1]}' is NOT 1234")
    print("-"*30)

conn.close()

print("\n" + "="*50)
print("Try logging in with:")
print("Admin: username='admin' password='1234'")
print("Teacher: username='teacher' password='1234'")
print("="*50)