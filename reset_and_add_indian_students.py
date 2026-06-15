import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# ==================== DELETE ALL EXISTING STUDENTS ====================
print("=" * 60)
print("🗑️ Deleting all existing students...")
print("=" * 60)

cur.execute("SELECT COUNT(*) FROM students")
old_count = cur.fetchone()[0]
print(f"📊 Old students count: {old_count}")

# Delete all students
cur.execute("DELETE FROM students")
print("✅ All old students deleted!")

# Reset auto-increment
cur.execute("DELETE FROM sqlite_sequence WHERE name='students'")
print("✅ ID sequence reset!")

# ==================== ADD INDIAN STUDENTS ====================

# B.Tech Students (8 Semesters) - 2 students per semester
btech_students = [
    # Semester 1
    ('Aarav Sharma', 'BT101', 'B.Tech (UG)', 1, 'aarav.sharma@email.com', '9876543201', 'default.png'),
    ('Ananya Verma', 'BT102', 'B.Tech (UG)', 1, 'ananya.verma@email.com', '9876543202', 'default.png'),
    # Semester 2
    ('Vihaan Gupta', 'BT201', 'B.Tech (UG)', 2, 'vihaan.gupta@email.com', '9876543203', 'default.png'),
    ('Saanvi Reddy', 'BT202', 'B.Tech (UG)', 2, 'saanvi.reddy@email.com', '9876543204', 'default.png'),
    # Semester 3
    ('Arjun Nair', 'BT301', 'B.Tech (UG)', 3, 'arjun.nair@email.com', '9876543205', 'default.png'),
    ('Diya Patil', 'BT302', 'B.Tech (UG)', 3, 'diya.patil@email.com', '9876543206', 'default.png'),
    # Semester 4
    ('Kabir Singh', 'BT401', 'B.Tech (UG)', 4, 'kabir.singh@email.com', '9876543207', 'default.png'),
    ('Iyer K', 'BT402', 'B.Tech (UG)', 4, 'ishita.iyer@email.com', '9876543208', 'default.png'),
    # Semester 5
    ('Reyansh Malhotra', 'BT501', 'B.Tech (UG)', 5, 'reyansh.malhotra@email.com', '9876543209', 'default.png'),
    ('Myra Kaur', 'BT502', 'B.Tech (UG)', 5, 'myra.kaur@email.com', '9876543210', 'default.png'),
    # Semester 6
    ('Advik Choudhary', 'BT601', 'B.Tech (UG)', 6, 'advik.choudhary@email.com', '9876543211', 'default.png'),
    ('Anvi Thakur', 'BT602', 'B.Tech (UG)', 6, 'anvi.thakur@email.com', '9876543212', 'default.png'),
    # Semester 7
    ('Pranav Joshi', 'BT701', 'B.Tech (UG)', 7, 'pranav.joshi@email.com', '9876543213', 'default.png'),
    ('Kiara Mehra', 'BT702', 'B.Tech (UG)', 7, 'kiara.mehra@email.com', '9876543214', 'default.png'),
    # Semester 8
    ('Rudra Shetty', 'BT801', 'B.Tech (UG)', 8, 'rudra.shetty@email.com', '9876543215', 'default.png'),
    ('Ahana Menon', 'BT802', 'B.Tech (UG)', 8, 'ahana.menon@email.com', '9876543216', 'default.png'),
]

# BCA Students (6 Semesters) - 2 students per semester
bca_students = [
    ('Aryan Kumar', 'BCA101', 'BCA (UG)', 1, 'aryan.kumar@email.com', '9876543301', 'default.png'),
    ('Tara Kapoor', 'BCA102', 'BCA (UG)', 1, 'tara.kapoor@email.com', '9876543302', 'default.png'),
    ('Daksh Bhatia', 'BCA201', 'BCA (UG)', 2, 'daksh.bhatia@email.com', '9876543303', 'default.png'),
    ('Zara Khan', 'BCA202', 'BCA (UG)', 2, 'zara.khan@email.com', '9876543304', 'default.png'),
    ('Atharv Saxena', 'BCA301', 'BCA (UG)', 3, 'atharv.saxena@email.com', '9876543305', 'default.png'),
    ('Riya Das', 'BCA302', 'BCA (UG)', 3, 'riya.das@email.com', '9876543306', 'default.png'),
    ('Shaurya Ghosh', 'BCA401', 'BCA (UG)', 4, 'shaurya.ghosh@email.com', '9876543307', 'default.png'),
    ('Pari Walia', 'BCA402', 'BCA (UG)', 4, 'pari.walia@email.com', '9876543308', 'default.png'),
    ('Krishna Iyengar', 'BCA501', 'BCA (UG)', 5, 'krishna.iyengar@email.com', '9876543309', 'default.png'),
    ('Mira Pillai', 'BCA502', 'BCA (UG)', 5, 'mira.pillai@email.com', '9876543310', 'default.png'),
    ('Yash Agarwal', 'BCA601', 'BCA (UG)', 6, 'yash.agarwal@email.com', '9876543311', 'default.png'),
    ('Ira Jain', 'BCA602', 'BCA (UG)', 6, 'ira.jain@email.com', '9876543312', 'default.png'),
]

# B.Com Students (6 Semesters) - 1 student per semester
bcom_students = [
    ('Lakshay Mittal', 'COM101', 'B.Com (UG)', 1, 'lakshay.mittal@email.com', '9876543401', 'default.png'),
    ('Navya Bansal', 'COM201', 'B.Com (UG)', 2, 'navya.bansal@email.com', '9876543402', 'default.png'),
    ('Dhruv Goyal', 'COM301', 'B.Com (UG)', 3, 'dhruv.goyal@email.com', '9876543403', 'default.png'),
    ('Tanvi Sethi', 'COM401', 'B.Com (UG)', 4, 'tanvi.sethi@email.com', '9876543404', 'default.png'),
    ('Aryan Khanna', 'COM501', 'B.Com (UG)', 5, 'aryan.khanna@email.com', '9876543405', 'default.png'),
    ('Kaira Chawla', 'COM601', 'B.Com (UG)', 6, 'kaira.chawla@email.com', '9876543406', 'default.png'),
]

# MCA Students (4 Semesters) - 2 students per semester
mca_students = [
    ('Dev Arora', 'MCA101', 'MCA (PG)', 1, 'dev.arora@email.com', '9876543601', 'default.png'),
    ('Sia Bhatnagar', 'MCA102', 'MCA (PG)', 1, 'sia.bhatnagar@email.com', '9876543602', 'default.png'),
    ('Tanay Puri', 'MCA201', 'MCA (PG)', 2, 'tanay.puri@email.com', '9876543603', 'default.png'),
    ('Aditi Sinha', 'MCA202', 'MCA (PG)', 2, 'aditi.sinha@email.com', '9876543604', 'default.png'),
    ('Yuvan Dutta', 'MCA301', 'MCA (PG)', 3, 'yuvan.dutta@email.com', '9876543605', 'default.png'),
    ('Sanaya Kohli', 'MCA302', 'MCA (PG)', 3, 'sanaya.kohli@email.com', '9876543606', 'default.png'),
    ('Ayaan Bhatt', 'MCA401', 'MCA (PG)', 4, 'ayaan.bhatt@email.com', '9876543607', 'default.png'),
    ('Sara Joseph', 'MCA402', 'MCA (PG)', 4, 'sara.joseph@email.com', '9876543608', 'default.png'),
]

# MBA Students (4 Semesters) - 1 student per semester
mba_students = [
    ('Samar Singhania', 'MBA101', 'MBA (PG)', 1, 'samar.singhania@email.com', '9876543701', 'default.png'),
    ('Riddhima Khurana', 'MBA201', 'MBA (PG)', 2, 'riddhima.khurana@email.com', '9876543702', 'default.png'),
    ('Arhaan Desai', 'MBA301', 'MBA (PG)', 3, 'arhaan.desai@email.com', '9876543703', 'default.png'),
    ('Navya Mishra', 'MBA401', 'MBA (PG)', 4, 'navya.mishra@email.com', '9876543704', 'default.png'),
]

# LLB Students (UG) - 3 Semesters only
llb_students = [
    ('Rohan Thakur', 'LLB101', 'LLB (UG)', 1, 'rohan.thakur@email.com', '9876543501', 'default.png'),
    ('Sanya Grover', 'LLB201', 'LLB (UG)', 2, 'sanya.grover@email.com', '9876543502', 'default.png'),
    ('Kunal Rajput', 'LLB301', 'LLB (UG)', 3, 'kunal.rajput@email.com', '9876543503', 'default.png'),
]

# M.Tech Students (PG) - 2 students per semester
mtech_students = [
    ('Nikhil Bhardwaj', 'MT101', 'M.Tech (PG)', 1, 'nikhil.bhardwaj@email.com', '9876543801', 'default.png'),
    ('Shreya Trivedi', 'MT102', 'M.Tech (PG)', 1, 'shreya.trivedi@email.com', '9876543802', 'default.png'),
    ('Aarush Kulkarni', 'MT201', 'M.Tech (PG)', 2, 'aarush.kulkarni@email.com', '9876543803', 'default.png'),
    ('Kavya Oak', 'MT202', 'M.Tech (PG)', 2, 'kavya.oak@email.com', '9876543804', 'default.png'),
    ('Reyansh Pendse', 'MT301', 'M.Tech (PG)', 3, 'reyansh.pendse@email.com', '9876543805', 'default.png'),
    ('Anika Surve', 'MT302', 'M.Tech (PG)', 3, 'anika.surve@email.com', '9876543806', 'default.png'),
    ('Shaunak Rane', 'MT401', 'M.Tech (PG)', 4, 'shaunak.rane@email.com', '9876543807', 'default.png'),
    ('Janhavi Vaidya', 'MT402', 'M.Tech (PG)', 4, 'janhavi.vaidya@email.com', '9876543808', 'default.png'),
]

# M.Sc Students (PG) - 2 students per semester
msc_students = [
    ('Anshuman Khare', 'MSC101', 'M.Sc (PG)', 1, 'anshuman.khare@email.com', '9876543901', 'default.png'),
    ('Tanushree Naik', 'MSC102', 'M.Sc (PG)', 1, 'tanushree.naik@email.com', '9876543902', 'default.png'),
    ('Samarth Shinde', 'MSC201', 'M.Sc (PG)', 2, 'samarth.shinde@email.com', '9876543903', 'default.png'),
    ('Niharika Mhatre', 'MSC202', 'M.Sc (PG)', 2, 'niharika.mhatre@email.com', '9876543904', 'default.png'),
]

# LLM Students (PG) - 2 students
llm_students = [
    ('Chinmay Kulkarni', 'LLM101', 'LLM (PG)', 1, 'chinmay.kulkarni@email.com', '9876544001', 'default.png'),
    ('Gayatri Deshpande', 'LLM102', 'LLM (PG)', 1, 'gayatri.deshpande@email.com', '9876544002', 'default.png'),
]

# Combine all students
all_students = (btech_students + bca_students + bcom_students + llb_students + 
                mca_students + mba_students + mtech_students + msc_students + llm_students)

# Insert all students
print("\n" + "=" * 60)
print("📚 Adding Indian Students...")
print("=" * 60)

count = 0
for name, roll_no, course, semester, email, phone, photo in all_students:
    try:
        cur.execute("""
            INSERT INTO students (name, roll_no, course, semester, email, phone, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, roll_no, course, semester, email, phone, photo))
        count += 1
        print(f"✅ Added: {name} ({roll_no}) - {course} (Sem {semester})")
    except sqlite3.IntegrityError:
        print(f"⚠️ {roll_no} already exists")

conn.commit()

# Show summary
print("\n" + "=" * 60)
print("📊 Final Summary")
print("=" * 60)

cur.execute("SELECT course, COUNT(*) FROM students GROUP BY course ORDER BY course")
courses = cur.fetchall()
for course, student_count in courses:
    print(f"   {course}: {student_count} students")

cur.execute("SELECT COUNT(*) FROM students")
total = cur.fetchone()[0]
print("\n" + "=" * 60)
print(f"✅ Total Students: {total}")
print("=" * 60)

conn.close()
print("\n✨ Done! All old students removed and new Indian students added!")
print("\n🔑 Student Login:")
print("   Username: Roll Number")
print("   Password: Email Address")