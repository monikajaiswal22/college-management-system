import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# Check duplicates
cur.execute("""
    SELECT name, course, semester, COUNT(*) 
    FROM subjects 
    GROUP BY name, course, semester 
    HAVING COUNT(*) > 1
""")
duplicates = cur.fetchall()

print("=" * 60)
print("Duplicate Subjects Found:")
print("=" * 60)
for dup in duplicates:
    print(f"  {dup[0]} - {dup[1]} (Sem {dup[2]}) - {dup[3]} times")

# Remove duplicates (keep one)
cur.execute("""
    DELETE FROM subjects 
    WHERE id NOT IN (
        SELECT MIN(id) 
        FROM subjects 
        GROUP BY name, course, semester
    )
""")
conn.commit()

print("\n✅ Duplicates removed!")

# Show remaining subjects
cur.execute("SELECT course, COUNT(*) FROM subjects GROUP BY course ORDER BY course")
courses = cur.fetchall()

print("\n" + "=" * 60)
print("Remaining Subjects:")
print("=" * 60)
for course, count in courses:
    print(f"  {course}: {count} subjects")

conn.close()