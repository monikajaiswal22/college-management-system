import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

# First, clear existing subjects (optional - comment if you want to keep old)
# cur.execute("DELETE FROM subjects")
# print("Old subjects cleared!")

# ==================== UG (UNDERGRADUATE) COURSES ====================

# B.Tech (8 Semesters)
btech_subjects = [
    # Semester 1
    ('Engineering Mathematics-I', 'B.Tech (UG)', 1),
    ('Engineering Physics', 'B.Tech (UG)', 1),
    ('Engineering Chemistry', 'B.Tech (UG)', 1),
    ('Programming for Problem Solving', 'B.Tech (UG)', 1),
    ('English Communication', 'B.Tech (UG)', 1),
    ('Basic Electrical Engineering', 'B.Tech (UG)', 1),
    # Semester 2
    ('Engineering Mathematics-II', 'B.Tech (UG)', 2),
    ('Engineering Mechanics', 'B.Tech (UG)', 2),
    ('Data Structures', 'B.Tech (UG)', 2),
    ('Object Oriented Programming', 'B.Tech (UG)', 2),
    ('Environmental Science', 'B.Tech (UG)', 2),
    ('Digital Electronics', 'B.Tech (UG)', 2),
    # Semester 3
    ('Discrete Mathematics', 'B.Tech (UG)', 3),
    ('Database Management Systems', 'B.Tech (UG)', 3),
    ('Computer Networks', 'B.Tech (UG)', 3),
    ('Operating Systems', 'B.Tech (UG)', 3),
    ('Software Engineering', 'B.Tech (UG)', 3),
    ('Microprocessors', 'B.Tech (UG)', 3),
    # Semester 4
    ('Design and Analysis of Algorithms', 'B.Tech (UG)', 4),
    ('Web Technologies', 'B.Tech (UG)', 4),
    ('Machine Learning', 'B.Tech (UG)', 4),
    ('Cloud Computing', 'B.Tech (UG)', 4),
    ('Cyber Security', 'B.Tech (UG)', 4),
    ('Theory of Computation', 'B.Tech (UG)', 4),
    # Semester 5
    ('Artificial Intelligence', 'B.Tech (UG)', 5),
    ('Big Data Analytics', 'B.Tech (UG)', 5),
    ('Internet of Things', 'B.Tech (UG)', 5),
    ('Mobile Application Development', 'B.Tech (UG)', 5),
    ('Computer Graphics', 'B.Tech (UG)', 5),
    ('Software Testing', 'B.Tech (UG)', 5),
    # Semester 6
    ('Blockchain Technology', 'B.Tech (UG)', 6),
    ('Data Science', 'B.Tech (UG)', 6),
    ('DevOps', 'B.Tech (UG)', 6),
    ('Cloud Security', 'B.Tech (UG)', 6),
    ('Project Management', 'B.Tech (UG)', 6),
    ('Industrial Training', 'B.Tech (UG)', 6),
    # Semester 7
    ('Deep Learning', 'B.Tech (UG)', 7),
    ('Natural Language Processing', 'B.Tech (UG)', 7),
    ('Robotics', 'B.Tech (UG)', 7),
    ('Quantum Computing', 'B.Tech (UG)', 7),
    ('Major Project - I', 'B.Tech (UG)', 7),
    # Semester 8
    ('Business Intelligence', 'B.Tech (UG)', 8),
    ('Ethical Hacking', 'B.Tech (UG)', 8),
    ('Augmented Reality', 'B.Tech (UG)', 8),
    ('Major Project - II', 'B.Tech (UG)', 8),
    ('Seminar', 'B.Tech (UG)', 8),
]

# BCA (6 Semesters)
bca_subjects = [
    # Semester 1
    ('Fundamentals of Computer', 'BCA (UG)', 1),
    ('Programming in C', 'BCA (UG)', 1),
    ('Digital Electronics', 'BCA (UG)', 1),
    ('Mathematics-I', 'BCA (UG)', 1),
    ('English Communication', 'BCA (UG)', 1),
    ('Computer Architecture', 'BCA (UG)', 1),
    # Semester 2
    ('Data Structures', 'BCA (UG)', 2),
    ('Database Management Systems', 'BCA (UG)', 2),
    ('Object Oriented Programming', 'BCA (UG)', 2),
    ('Mathematics-II', 'BCA (UG)', 2),
    ('Operating Systems', 'BCA (UG)', 2),
    ('Web Design', 'BCA (UG)', 2),
    # Semester 3
    ('Computer Networks', 'BCA (UG)', 3),
    ('Web Technologies', 'BCA (UG)', 3),
    ('Software Engineering', 'BCA (UG)', 3),
    ('Python Programming', 'BCA (UG)', 3),
    ('Multimedia Systems', 'BCA (UG)', 3),
    ('Statistics', 'BCA (UG)', 3),
    # Semester 4
    ('Java Programming', 'BCA (UG)', 4),
    ('Cloud Computing', 'BCA (UG)', 4),
    ('Cyber Security', 'BCA (UG)', 4),
    ('Mobile Computing', 'BCA (UG)', 4),
    ('Data Mining', 'BCA (UG)', 4),
    ('E-Commerce', 'BCA (UG)', 4),
    # Semester 5
    ('Machine Learning', 'BCA (UG)', 5),
    ('Internet of Things', 'BCA (UG)', 5),
    ('Big Data Analytics', 'BCA (UG)', 5),
    ('Software Testing', 'BCA (UG)', 5),
    ('Project - I', 'BCA (UG)', 5),
    # Semester 6
    ('Artificial Intelligence', 'BCA (UG)', 6),
    ('Blockchain Technology', 'BCA (UG)', 6),
    ('DevOps', 'BCA (UG)', 6),
    ('Data Science', 'BCA (UG)', 6),
    ('Major Project', 'BCA (UG)', 6),
]

# B.Com (6 Semesters)
bcom_subjects = [
    # Semester 1
    ('Financial Accounting', 'B.Com (UG)', 1),
    ('Business Economics', 'B.Com (UG)', 1),
    ('Business Mathematics', 'B.Com (UG)', 1),
    ('Business Communication', 'B.Com (UG)', 1),
    ('Principles of Management', 'B.Com (UG)', 1),
    ('Computer Applications', 'B.Com (UG)', 1),
    # Semester 2
    ('Corporate Accounting', 'B.Com (UG)', 2),
    ('Cost Accounting', 'B.Com (UG)', 2),
    ('Business Statistics', 'B.Com (UG)', 2),
    ('Marketing Management', 'B.Com (UG)', 2),
    ('Income Tax', 'B.Com (UG)', 2),
    ('Environmental Studies', 'B.Com (UG)', 2),
    # Semester 3
    ('Advanced Accounting', 'B.Com (UG)', 3),
    ('Goods and Services Tax', 'B.Com (UG)', 3),
    ('Management Accounting', 'B.Com (UG)', 3),
    ('Business Law', 'B.Com (UG)', 3),
    ('Human Resource Management', 'B.Com (UG)', 3),
    ('Financial Management', 'B.Com (UG)', 3),
    # Semester 4
    ('Auditing', 'B.Com (UG)', 4),
    ('Corporate Law', 'B.Com (UG)', 4),
    ('International Business', 'B.Com (UG)', 4),
    ('Entrepreneurship', 'B.Com (UG)', 4),
    ('Banking and Insurance', 'B.Com (UG)', 4),
    ('E-Business', 'B.Com (UG)', 4),
    # Semester 5
    ('Financial Services', 'B.Com (UG)', 5),
    ('Investment Management', 'B.Com (UG)', 5),
    ('Strategic Management', 'B.Com (UG)', 5),
    ('Project Management', 'B.Com (UG)', 5),
    ('Research Methodology', 'B.Com (UG)', 5),
    # Semester 6
    ('International Finance', 'B.Com (UG)', 6),
    ('Financial Derivatives', 'B.Com (UG)', 6),
    ('Business Ethics', 'B.Com (UG)', 6),
    ('Digital Marketing', 'B.Com (UG)', 6),
    ('Major Project', 'B.Com (UG)', 6),
]

# LLB (6 Semesters)
llb_subjects = [
    # Semester 1
    ('Constitutional Law', 'LLB (UG)', 1),
    ('Legal Method', 'LLB (UG)', 1),
    ('Law of Torts', 'LLB (UG)', 1),
    ('Criminal Law', 'LLB (UG)', 1),
    ('Contract Law', 'LLB (UG)', 1),
    ('Legal Writing', 'LLB (UG)', 1),
    # Semester 2
    ('Family Law', 'LLB (UG)', 2),
    ('Property Law', 'LLB (UG)', 2),
    ('Administrative Law', 'LLB (UG)', 2),
    ('Company Law', 'LLB (UG)', 2),
    ('Environmental Law', 'LLB (UG)', 2),
    ('Human Rights Law', 'LLB (UG)', 2),
    # Semester 3
    ('Criminal Procedure Code', 'LLB (UG)', 3),
    ('Civil Procedure Code', 'LLB (UG)', 3),
    ('Labour Law', 'LLB (UG)', 3),
    ('Taxation Law', 'LLB (UG)', 3),
    ('Evidence Law', 'LLB (UG)', 3),
    ('Jurisprudence', 'LLB (UG)', 3),
    # Semester 4
    ('Intellectual Property Law', 'LLB (UG)', 4),
    ('International Law', 'LLB (UG)', 4),
    ('Cyber Law', 'LLB (UG)', 4),
    ('Banking Law', 'LLB (UG)', 4),
    ('Moot Court', 'LLB (UG)', 4),
    ('Drafting and Pleading', 'LLB (UG)', 4),
    # Semester 5
    ('Professional Ethics', 'LLB (UG)', 5),
    ('Alternative Dispute Resolution', 'LLB (UG)', 5),
    ('Interpretation of Statutes', 'LLB (UG)', 5),
    ('Clinical Course', 'LLB (UG)', 5),
    # Semester 6
    ('Land Laws', 'LLB (UG)', 6),
    ('Women and Law', 'LLB (UG)', 6),
    ('Internship', 'LLB (UG)', 6),
    ('Project Work', 'LLB (UG)', 6),
]

# ==================== PG (POSTGRADUATE) COURSES ====================

# MCA (4 Semesters)
mca_subjects = [
    # Semester 1
    ('Advanced Programming', 'MCA (PG)', 1),
    ('Data Structures and Algorithms', 'MCA (PG)', 1),
    ('Database Management Systems', 'MCA (PG)', 1),
    ('Operating Systems', 'MCA (PG)', 1),
    ('Computer Networks', 'MCA (PG)', 1),
    ('Python Programming', 'MCA (PG)', 1),
    ('Mathematical Foundation', 'MCA (PG)', 1),
    # Semester 2
    ('Web Technologies', 'MCA (PG)', 2),
    ('Software Engineering', 'MCA (PG)', 2),
    ('Cloud Computing', 'MCA (PG)', 2),
    ('Machine Learning', 'MCA (PG)', 2),
    ('Mobile App Development', 'MCA (PG)', 2),
    ('Java Programming', 'MCA (PG)', 2),
    ('Database Administration', 'MCA (PG)', 2),
    # Semester 3
    ('Big Data Analytics', 'MCA (PG)', 3),
    ('Cyber Security', 'MCA (PG)', 3),
    ('Artificial Intelligence', 'MCA (PG)', 3),
    ('Internet of Things', 'MCA (PG)', 3),
    ('Data Science', 'MCA (PG)', 3),
    ('Project - I', 'MCA (PG)', 3),
    # Semester 4
    ('Blockchain Technology', 'MCA (PG)', 4),
    ('DevOps', 'MCA (PG)', 4),
    ('Natural Language Processing', 'MCA (PG)', 4),
    ('Deep Learning', 'MCA (PG)', 4),
    ('Major Project', 'MCA (PG)', 4),
    ('Seminar', 'MCA (PG)', 4),
]

# M.Tech (4 Semesters)
mtech_subjects = [
    # Semester 1
    ('Advanced Mathematics', 'M.Tech (PG)', 1),
    ('Research Methodology', 'M.Tech (PG)', 1),
    ('Advanced Data Structures', 'M.Tech (PG)', 1),
    ('Machine Learning Techniques', 'M.Tech (PG)', 1),
    ('Cloud Architecture', 'M.Tech (PG)', 1),
    ('Advanced Algorithms', 'M.Tech (PG)', 1),
    # Semester 2
    ('Big Data Analytics', 'M.Tech (PG)', 2),
    ('Internet of Things', 'M.Tech (PG)', 2),
    ('Cyber Security Frameworks', 'M.Tech (PG)', 2),
    ('Deep Learning', 'M.Tech (PG)', 2),
    ('Project Management', 'M.Tech (PG)', 2),
    ('Research Paper Writing', 'M.Tech (PG)', 2),
    # Semester 3
    ('Thesis - I', 'M.Tech (PG)', 3),
    ('Seminar', 'M.Tech (PG)', 3),
    ('Elective - I', 'M.Tech (PG)', 3),
    ('Elective - II', 'M.Tech (PG)', 3),
    # Semester 4
    ('Thesis - II', 'M.Tech (PG)', 4),
    ('Viva Voce', 'M.Tech (PG)', 4),
]

# MBA (4 Semesters)
mba_subjects = [
    # Semester 1
    ('Principles of Management', 'MBA (PG)', 1),
    ('Organizational Behaviour', 'MBA (PG)', 1),
    ('Managerial Economics', 'MBA (PG)', 1),
    ('Financial Accounting', 'MBA (PG)', 1),
    ('Marketing Management', 'MBA (PG)', 1),
    ('Business Communication', 'MBA (PG)', 1),
    ('Quantitative Methods', 'MBA (PG)', 1),
    # Semester 2
    ('Human Resource Management', 'MBA (PG)', 2),
    ('Operations Management', 'MBA (PG)', 2),
    ('Business Research Methods', 'MBA (PG)', 2),
    ('Corporate Finance', 'MBA (PG)', 2),
    ('Strategic Management', 'MBA (PG)', 2),
    ('Business Analytics', 'MBA (PG)', 2),
    ('Legal Environment', 'MBA (PG)', 2),
    # Semester 3
    ('Digital Marketing', 'MBA (PG)', 3),
    ('Supply Chain Management', 'MBA (PG)', 3),
    ('Entrepreneurship', 'MBA (PG)', 3),
    ('International Business', 'MBA (PG)', 3),
    ('Summer Internship', 'MBA (PG)', 3),
    # Semester 4
    ('Project Work', 'MBA (PG)', 4),
    ('Viva Voce', 'MBA (PG)', 4),
    ('Elective - I', 'MBA (PG)', 4),
    ('Elective - II', 'MBA (PG)', 4),
]

# M.Sc (4 Semesters)
msc_subjects = [
    # Semester 1
    ('Advanced Mathematics', 'M.Sc (PG)', 1),
    ('Research Methodology', 'M.Sc (PG)', 1),
    ('Computer Applications', 'M.Sc (PG)', 1),
    ('Data Analysis', 'M.Sc (PG)', 1),
    ('Scientific Computing', 'M.Sc (PG)', 1),
    ('Statistics', 'M.Sc (PG)', 1),
    # Semester 2
    ('Machine Learning', 'M.Sc (PG)', 2),
    ('Big Data Analytics', 'M.Sc (PG)', 2),
    ('Bioinformatics', 'M.Sc (PG)', 2),
    ('Statistical Methods', 'M.Sc (PG)', 2),
    ('Research Paper', 'M.Sc (PG)', 2),
    # Semester 3
    ('Thesis - I', 'M.Sc (PG)', 3),
    ('Seminar', 'M.Sc (PG)', 3),
    ('Elective - I', 'M.Sc (PG)', 3),
    # Semester 4
    ('Thesis - II', 'M.Sc (PG)', 4),
    ('Viva Voce', 'M.Sc (PG)', 4),
]

# LLM (4 Semesters)
llm_subjects = [
    # Semester 1
    ('Constitutional Law', 'LLM (PG)', 1),
    ('Criminal Law', 'LLM (PG)', 1),
    ('International Law', 'LLM (PG)', 1),
    ('Human Rights Law', 'LLM (PG)', 1),
    ('Legal Research', 'LLM (PG)', 1),
    # Semester 2
    ('Corporate Law', 'LLM (PG)', 2),
    ('Cyber Law', 'LLM (PG)', 2),
    ('Environmental Law', 'LLM (PG)', 2),
    ('Intellectual Property Rights', 'LLM (PG)', 2),
    ('Comparative Law', 'LLM (PG)', 2),
    # Semester 3
    ('Dissertation - I', 'LLM (PG)', 3),
    ('Seminar', 'LLM (PG)', 3),
    ('Elective - I', 'LLM (PG)', 3),
    # Semester 4
    ('Dissertation - II', 'LLM (PG)', 4),
    ('Viva Voce', 'LLM (PG)', 4),
]

# All subjects combined
all_subjects = (btech_subjects + bca_subjects + bcom_subjects + llb_subjects + 
                mca_subjects + mtech_subjects + mba_subjects + msc_subjects + llm_subjects)

# Insert all subjects
print("=" * 70)
print("📚 Adding Complete Courses with All Semesters")
print("=" * 70)

count = 0
for name, course, semester in all_subjects:
    try:
        cur.execute("INSERT INTO subjects (name, course, semester) VALUES (?, ?, ?)", 
                   (name, course, semester))
        count += 1
        print(f"✅ Added: {name} - {course} (Sem {semester})")
    except Exception as e:
        print(f"⚠️ Error: {name} - {e}")

conn.commit()

# Show summary
cur.execute("SELECT course, MIN(semester) as min_sem, MAX(semester) as max_sem, COUNT(*) FROM subjects GROUP BY course ORDER BY course")
courses = cur.fetchall()

print("\n" + "=" * 70)
print("📊 Course-wise Subjects Summary")
print("=" * 70)
for course, min_sem, max_sem, subj_count in courses:
    print(f"   {course}: {subj_count} subjects (Semester {min_sem} to {max_sem})")

cur.execute("SELECT COUNT(*) FROM subjects")
total = cur.fetchone()[0]
print("\n" + "=" * 70)
print(f"✅ Total Subjects Added: {total}")
print("=" * 70)

conn.close()
print("\n✨ All courses with complete semesters added successfully!")