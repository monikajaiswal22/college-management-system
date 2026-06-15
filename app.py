from flask import Flask, render_template, request, redirect, session, Response, send_file
import sqlite3, os, csv
from io import BytesIO
from reportlab.pdfgen import canvas
from werkzeug.utils import secure_filename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, timedelta
import calendar
import os

EMAIL = os.environ.get('EMAIL', 'your_email@gmail.com')
APP_PASSWORD = os.environ.get('APP_PASSWORD', 'your_app_password')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = os.environ.get('SECRET_KEY', 'secret123')

# Create upload folder if not exists
UPLOAD_FOLDER = '/tmp/uploads' if os.environ.get('RENDER') else 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ---------------- DB ----------------
def connect_db():
    db_path = os.environ.get('DATABASE_PATH', 'database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)
    
    # Teachers table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        department TEXT,
        qualification TEXT,
        email TEXT,
        photo TEXT
    )
    """)

    # Insert sample teachers
    cur.execute("SELECT * FROM teachers LIMIT 1")
    if not cur.fetchone():
        cur.execute("""
        INSERT INTO teachers (name, department, qualification, email) VALUES 
        ('Dr. Rajesh Kumar', 'Computer Science', 'Ph.D (IIT Delhi)', 'rajesh@elite.edu'),
        ('Prof. Priya Sharma', 'Management', 'MBA (IIM Ahmedabad)', 'priya@elite.edu'),
        ('Dr. Ankit Verma', 'Data Science', 'Ph.D (MIT)', 'ankit@elite.edu')
        """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS notices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        date TEXT,
        type TEXT
    )
    """)

    cur.execute("SELECT * FROM notices LIMIT 1")
    if not cur.fetchone():
        today = date.today().isoformat()
        cur.execute("""
        INSERT INTO notices (title, content, date, type) VALUES 
        ('Admissions Open 2026', 'Applications for B.Tech, MBA, BCA are now open. Last date: March 31, 2026', ?, 'notice'),
        ('Annual Tech Fest 2026', 'Join us for the biggest tech fest on April 15-16, 2026', ?, 'event'),
        ('Exam Schedule Released', 'End semester examinations will begin from April 20, 2026', ?, 'notice')
        """, (today, today, today))

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll_no TEXT UNIQUE,
        course TEXT,
        semester INTEGER,
        email TEXT,
        phone INTEGER,        
        photo TEXT
    )
    """)

    # 📚 SUBJECTS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        semester INTEGER
    )
    """)
   
    # 📅 ATTENDANCE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        date TEXT,
        status TEXT,
        UNIQUE(student_id, subject_id, date)
    )
    """)

    # 📝 MARKS
    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT,
        marks INTEGER,
        total INTEGER,
        added_by TEXT
    )
    """)   

    cur.execute("""
    CREATE TABLE IF NOT EXISTS fees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        amount INTEGER,
        date TEXT,
        status TEXT
    )
    """)

    # ✅ USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # ✅ Default users
    cur.execute("SELECT * FROM users WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                   ('admin', generate_password_hash('1234'), 'admin'))
    
    cur.execute("SELECT * FROM users WHERE username='teacher'")
    if not cur.fetchone():
        cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                   ('teacher', generate_password_hash('1234'), 'teacher'))

    conn.commit()
    conn.close()

init_db()

# ---------------- EMAIL ----------------
def send_email(receiver_email, subject, message):
    try:
        sender = EMAIL
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, APP_PASSWORD)
        server.sendmail(sender, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print("❌ Email error:", e)

# ---------------send fee remainder--------------
@app.route("/send-fee-reminder")
def send_fee_reminder():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    SELECT students.name, students.email, fees.amount
    FROM students
    JOIN fees ON students.id = fees.student_id
    WHERE fees.status = 'Pending'
    AND students.email IS NOT NULL AND students.email != ''
    """)
    rows = cur.fetchall()
    for row in rows:
        message = f"Dear {row['name']},\n\nYour fee of ₹{row['amount']} is pending. Please pay at the earliest.\n\nRegards,\nCollege Administration"
        send_email(row["email"], "Fee Reminder", message)
    conn.close()
    return "✅ Fee reminders sent successfully!"

# ------------download students---------------
@app.route("/download-students-pdf")
def download_pdf():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(200, 800, "STUDENTS REPORT")
    y = 750
    for row in data:
        pdf.drawString(50, y, f"{row['name']} - {row['course']} Sem {row['semester']}")
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 800
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="students.pdf", mimetype="application/pdf")

# ---------------export students--------------
@app.route("/export-students")
def export_students():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    def generate():
        yield "ID,Name,Roll No,Course,Semester,Email,Phone,Photo\n"
        for row in data:
            yield f"{row['id']},{row['name']},{row['roll_no']},{row['course']},{row['semester']},{row['email']},{row['phone']},{row['photo']}\n"
    return Response(generate(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=students.csv"})

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    # ---------------- LAST 7 DAYS ATTENDANCE ----------------
    dates = []
    present_data = []
    for i in range(6, -1, -1):
        day = datetime.now() - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        dates.append(day.strftime("%d %b"))
        cur.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Present'", (day_str,))
        count = cur.fetchone()[0]
        present_data.append(count)
    # ---------------- MONTHLY ATTENDANCE ----------------
    cur.execute("SELECT strftime('%m', date) as month, COUNT(*) FROM attendance WHERE status='Present' GROUP BY month")
    monthly = cur.fetchall()
    months = []
    monthly_data = []
    for m in monthly:
        months.append(calendar.month_name[int(m[0])])
        monthly_data.append(m[1])
    # ---------------- TODAY ATTENDANCE ----------------
    today = date.today()
    cur.execute("SELECT COUNT(*) FROM attendance WHERE date=?", (today,))
    today_total = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Present'", (today,))
    today_present = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Absent'", (today,))
    today_absent = cur.fetchone()[0] or 0
    today_percent = round((today_present / today_total) * 100, 2) if today_total else 0
    # ---------------- STUDENTS ----------------
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0] or 0
    # ---------------- FEES ----------------
    cur.execute("SELECT SUM(amount) FROM fees WHERE status='Paid'")
    total_fees = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(amount) FROM fees WHERE status='Pending'")
    pending_fees = cur.fetchone()[0] or 0
    # ---------------- ATTENDANCE OVERALL ----------------
    cur.execute("SELECT COUNT(*) FROM attendance")
    total_att = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present_att = cur.fetchone()[0] or 0
    attendance_percent = round((present_att / total_att) * 100, 2) if total_att else 0
    # ---------------- OVERALL MARKS ----------------
    cur.execute("SELECT AVG(marks) FROM marks")
    overall_percent = cur.fetchone()[0] or 0
    conn.close()
    return render_template("dashboard.html",
        total_students=total_students,
        total_fees=total_fees,
        pending_fees=pending_fees,
        attendance_percent=attendance_percent,
        overall_percent=overall_percent,
        dates=dates,
        present_data=present_data,
        months=months,
        monthly_data=monthly_data,
        today_total=today_total,
        today_present=today_present,
        today_absent=today_absent,
        today_percent=today_percent
    )

# ---------------- STUDENTS ----------------
@app.route("/students", methods=["GET","POST"])
def students():
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form.get('name')
        roll_no = request.form.get('roll_no')
        course = request.form.get('course')
        semester = request.form.get('semester')
        email = request.form.get('email')
        phone = request.form.get('phone')
        file = request.files.get('photo')
        filename = "default.png"
        if file and file.filename != "":
            os.makedirs("static/uploads", exist_ok=True)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cur.execute("INSERT INTO students(name,roll_no,course,semester,email,phone,photo) VALUES (?,?,?,?,?,?,?)", (name, roll_no, course, semester, email, phone, filename))
        conn.commit()
        return redirect("/students")
    cur.execute("SELECT * FROM students ORDER BY id DESC")
    students = cur.fetchall()
    conn.close()
    return render_template("students.html", students=students)

#-----------------student---------------------
@app.route("/student/<int:id>")
def student_profile(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    cur.execute("SELECT date,status FROM attendance WHERE student_id=?", (id,))
    attendance = cur.fetchall()
    cur.execute("SELECT amount,date,status FROM fees WHERE student_id=?", (id,))
    fees = cur.fetchall()
    conn.close()
    return render_template("student_profile.html", student=student, attendance=attendance, fees=fees)

# ----------------search_student--------------
@app.route("/search-students")
def search_students():
    if session.get('role') != 'admin':
        return ""
    conn = connect_db()
    cur = conn.cursor()
    q = request.args.get("q", "")
    cur.execute("SELECT * FROM students WHERE name LIKE ? OR roll_no LIKE ? ORDER BY name", (f"%{q}%", f"%{q}%"))
    students = cur.fetchall()
    conn.close()
    html = ""
    for s in students:
        html += f"""
        <tr>
            <td>{s["id"]}</td>
            <td><img src="/static/uploads/{s["photo"]}" width="40" style="border-radius:50%"></td>
            <td>{s["name"]}</td>
            <td>{s["roll_no"]}</td>
            <td>{s["course"]}</td>
            <td>{s["semester"]}</td>
            <td>{s["email"]}</td>
            <td>{s["phone"]}</td>
            <td>
                <a href="/student/{s['id']}" class="btn btn-info btn-sm">View</a>
                <a href="/edit-student/{s['id']}" class="btn btn-warning btn-sm">Edit</a>
                <a href="/delete-student/{s['id']}" class="btn btn-danger btn-sm" onclick="return confirm('Delete?')">Delete</a>
            </td>
        </table>
        """
    return html

# ---------------SUBJECT MANAGEMENT-----------
@app.route("/subjects", methods=["GET","POST"])
def subjects():
    conn = connect_db()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form['name']
        course = request.form['course']
        semester = request.form['semester']
        cur.execute("INSERT INTO subjects(name,course,semester) VALUES (?,?,?)", (name, course, semester))
        conn.commit()
    cur.execute("SELECT * FROM subjects")
    data = cur.fetchall()
    conn.close()
    return render_template("subjects.html", subjects=data)

# ================ EDIT SUBJECT =================
@app.route("/edit-subject/<int:id>", methods=["GET", "POST"])
def edit_subject(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form['name']
        course = request.form['course']
        semester = request.form['semester']
        cur.execute("UPDATE subjects SET name=?, course=?, semester=? WHERE id=?", (name, course, semester, id))
        conn.commit()
        conn.close()
        return redirect("/subjects")
    cur.execute("SELECT * FROM subjects WHERE id=?", (id,))
    subject = cur.fetchone()
    conn.close()
    return render_template("edit_subject.html", subject=subject)

# ================ DELETE SUBJECT =================
@app.route("/delete-subject/<int:id>")
def delete_subject(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM subjects WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/subjects")

# ---------------- ATTENDANCE (Teacher) ----------------
@app.route("/attendance", methods=["GET", "POST"])
def attendance():
    if 'role' not in session or session['role'] != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    subject_id = request.args.get('subject_id') or request.form.get('subject_id')
    cur.execute("SELECT * FROM subjects ORDER BY course, semester")
    subjects = cur.fetchall()
    students = []
    selected_subject = None
    if subject_id:
        cur.execute("SELECT * FROM subjects WHERE id=?", (subject_id,))
        selected_subject = cur.fetchone()
        if selected_subject:
            cur.execute("SELECT * FROM students ORDER BY name")
            students = cur.fetchall()
    if request.method == "POST":
        date = request.form.get("date")
        subject_id = request.form.get("subject_id")
        if subject_id and date:
            cur.execute("SELECT id FROM students")
            all_students = cur.fetchall()
            for s in all_students:
                status = request.form.get(f"status_{s['id']}")
                if status in ["Present", "Absent"]:
                    cur.execute("SELECT id FROM attendance WHERE student_id=? AND subject_id=? AND date=?", (s['id'], subject_id, date))
                    existing = cur.fetchone()
                    if existing:
                        cur.execute("UPDATE attendance SET status=? WHERE student_id=? AND subject_id=? AND date=?", (status, s['id'], subject_id, date))
                    else:
                        cur.execute("INSERT INTO attendance(student_id, subject_id, date, status) VALUES (?,?,?,?)", (s['id'], subject_id, date, status))
            conn.commit()
            return redirect(f"/attendance?subject_id={subject_id}")
    cur.execute("""
        SELECT attendance.id, students.name, subjects.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON students.id = attendance.student_id
        JOIN subjects ON subjects.id = attendance.subject_id
        ORDER BY attendance.date DESC
        LIMIT 50
    """)
    records = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM attendance")
    total = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present = cur.fetchone()[0] or 0
    attendance_percent = round((present / total) * 100, 2) if total else 0
    conn.close()
    return render_template("attendance.html",
        subjects=subjects,
        students=students,
        records=records,
        attendance_percent=attendance_percent,
        selected_subject=selected_subject
    )

# Update attendance
@app.route("/update-attendance/<int:id>/<status>")
def update_attendance(id, status):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE attendance SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT subject_id FROM attendance WHERE id=?", (id,))
    result = cur.fetchone()
    subject_id = result['subject_id'] if result else None
    conn.close()
    if subject_id:
        return redirect(f"/attendance?subject_id={subject_id}")
    return redirect("/attendance")

# Delete attendance
@app.route("/delete-attendance/<int:id>")
def delete_attendance(id):
    if 'role' not in session or session['role'] != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT subject_id FROM attendance WHERE id=?", (id,))
    result = cur.fetchone()
    subject_id = result['subject_id'] if result else None
    cur.execute("DELETE FROM attendance WHERE id=?", (id,))
    conn.commit()
    conn.close()
    if subject_id:
        return redirect(f"/attendance?subject_id={subject_id}")
    return redirect("/attendance")

# ================ TEACHER SUBJECTS PAGE ================
@app.route("/teacher-subjects")
def teacher_subjects():
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM subjects")
    subjects = cur.fetchall()
    conn.close()
    return render_template("teacher_subjects.html", subjects=subjects)

# Teacher View Student Profile
@app.route("/teacher-view-student/<int:id>")
def teacher_view_student(id):
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template("teacher_view_student.html", student=student)

# Admin View Student Profile
@app.route("/admin-view-student/<int:id>")
def admin_view_student(id):
    if session.get('role') != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template("admin_view_student.html", student=student)

# ---------------- TEACHER ATTENDANCE ----------------
@app.route("/teacher-attendance", methods=["GET", "POST"])
def teacher_attendance():
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    subject_id = request.args.get('subject_id')
    if request.method == "POST":
        subject_id = request.form.get('subject_id')
    cur.execute("SELECT * FROM subjects")
    subjects = cur.fetchall()
    students = []
    selected_subject = None
    if subject_id:
        cur.execute("SELECT * FROM subjects WHERE id=?", (subject_id,))
        selected_subject = cur.fetchone()
        if selected_subject:
            cur.execute("SELECT * FROM students ORDER BY name")
            students = cur.fetchall()
    if request.method == "POST":
        date = request.form.get('date')
        subject_id = request.form.get('subject_id')
        if date and subject_id:
            cur.execute("SELECT id FROM students")
            all_students = cur.fetchall()
            for s in all_students:
                status = request.form.get(f"status_{s['id']}")
                if status in ["Present", "Absent"]:
                    cur.execute("SELECT id FROM attendance WHERE student_id=? AND subject_id=? AND date=?", (s['id'], subject_id, date))
                    existing = cur.fetchone()
                    if existing:
                        cur.execute("UPDATE attendance SET status=? WHERE student_id=? AND subject_id=? AND date=?", (status, s['id'], subject_id, date))
                    else:
                        cur.execute("INSERT INTO attendance(student_id, subject_id, date, status) VALUES (?,?,?,?)", (s['id'], subject_id, date, status))
            conn.commit()
            conn.close()
            return redirect(f"/teacher-attendance?subject_id={subject_id}")
    cur.execute("""
        SELECT attendance.id, students.name, subjects.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON students.id = attendance.student_id
        JOIN subjects ON subjects.id = attendance.subject_id
        ORDER BY attendance.date DESC
        LIMIT 50
    """)
    records = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM attendance")
    total = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present = cur.fetchone()[0] or 0
    attendance_percent = round((present / total) * 100, 2) if total else 0
    conn.close()
    return render_template("teacher_attendance.html", 
                          subjects=subjects, 
                          students=students, 
                          records=records, 
                          attendance_percent=attendance_percent,
                          selected_subject=selected_subject)

# ================ ADMIN ATTENDANCE ================
@app.route("/admin-attendance", methods=["GET","POST"])
def admin_attendance():
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    subject_id = request.args.get('subject_id') or request.form.get('subject_id')
    cur.execute("SELECT * FROM subjects")
    subjects = cur.fetchall()
    students = []
    selected_subject = None
    if subject_id:
        cur.execute("SELECT * FROM subjects WHERE id=?", (subject_id,))
        selected_subject = cur.fetchone()
        if selected_subject:
            cur.execute("SELECT * FROM students WHERE course = ? AND semester = ? ORDER BY name", 
                       (selected_subject['course'], selected_subject['semester']))
            students = cur.fetchall()
    if request.method == "POST":
        date = request.form.get("date")
        subject_id = request.form.get("subject_id")
        cur.execute("SELECT course, semester FROM subjects WHERE id=?", (subject_id,))
        subj = cur.fetchone()
        if subj:
            cur.execute("SELECT id FROM students WHERE course=? AND semester=?", (subj['course'], subj['semester']))
            course_students = cur.fetchall()
            for s in course_students:
                status = request.form.get(f"status_{s['id']}")
                if status in ["Present", "Absent"]:
                    cur.execute("SELECT id FROM attendance WHERE student_id=? AND subject_id=? AND date=?", (s['id'], subject_id, date))
                    existing = cur.fetchone()
                    if existing:
                        cur.execute("UPDATE attendance SET status=? WHERE student_id=? AND subject_id=? AND date=?", (status, s['id'], subject_id, date))
                    else:
                        cur.execute("INSERT INTO attendance(student_id, subject_id, date, status) VALUES (?,?,?,?)", (s['id'], subject_id, date, status))
        conn.commit()
        return redirect("/admin-attendance")
    cur.execute("""
        SELECT attendance.id, students.name, subjects.name, attendance.date, attendance.status
        FROM attendance
        JOIN students ON students.id = attendance.student_id
        JOIN subjects ON subjects.id = attendance.subject_id
        ORDER BY attendance.date DESC
    """)
    records = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM attendance")
    total = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present = cur.fetchone()[0] or 0
    attendance_percent = round((present / total) * 100, 2) if total else 0
    conn.close()
    return render_template("admin_attendance.html", 
                          subjects=subjects, 
                          students=students, 
                          records=records, 
                          attendance_percent=attendance_percent,
                          selected_subject=selected_subject)

@app.route("/teacher-update-attendance/<int:id>/<status>")
def teacher_update_attendance(id, status):
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT subject_id FROM attendance WHERE id=?", (id,))
    result = cur.fetchone()
    subject_id = result['subject_id'] if result else None
    cur.execute("UPDATE attendance SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()
    if subject_id:
        return redirect(f"/teacher-attendance?subject_id={subject_id}")
    return redirect("/teacher-attendance")

@app.route("/teacher-delete-attendance/<int:id>")
def teacher_delete_attendance(id):
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT subject_id FROM attendance WHERE id=?", (id,))
    result = cur.fetchone()
    subject_id = result['subject_id'] if result else None
    cur.execute("DELETE FROM attendance WHERE id=?", (id,))
    conn.commit()
    conn.close()
    if subject_id:
        return redirect(f"/teacher-attendance?subject_id={subject_id}")
    return redirect("/teacher-attendance")

@app.route("/admin-update-attendance/<int:id>/<status>")
def admin_update_attendance(id, status):
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE attendance SET status=? WHERE id=?", (status, id))
    conn.commit()
    conn.close()
    return redirect("/admin-attendance")

@app.route("/admin-delete-attendance/<int:id>")
def admin_delete_attendance(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM attendance WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin-attendance")

#--------------- FEES ----------------
@app.route("/fees", methods=["GET","POST"])
def fees():
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    if request.method == "POST":
        cur.execute("INSERT INTO fees(student_id, amount, date, status) VALUES (?,?,?,?)", (request.form['student_id'], request.form['amount'], request.form['date'], request.form['status']))
        conn.commit()
    cur.execute("""
        SELECT fees.id, students.name, students.roll_no, fees.amount, fees.date, fees.status
        FROM fees
        JOIN students ON students.id = fees.student_id
        ORDER BY fees.id DESC
    """)
    records = cur.fetchall()
    cur.execute("SELECT SUM(amount) FROM fees")
    total_fees = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(amount) FROM fees WHERE status='Paid'")
    paid_fees = cur.fetchone()[0] or 0
    cur.execute("SELECT SUM(amount) FROM fees WHERE status='Pending'")
    pending_fees = cur.fetchone()[0] or 0
    conn.close()
    return render_template("fees.html", students=students, records=records, total_fees=total_fees, paid_fees=paid_fees, pending_fees=pending_fees)

# ================ EDIT FEE =================
@app.route("/edit-fee/<int:id>", methods=["GET", "POST"])
def edit_fee(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if request.method == "POST":
        student_id = request.form['student_id']
        amount = request.form['amount']
        date = request.form['date']
        status = request.form['status']
        cur.execute("UPDATE fees SET student_id=?, amount=?, date=?, status=? WHERE id=?", (student_id, amount, date, status, id))
        conn.commit()
        conn.close()
        return redirect("/fees")
    cur.execute("SELECT fees.*, students.name, students.roll_no FROM fees JOIN students ON students.id = fees.student_id WHERE fees.id=?", (id,))
    fee = cur.fetchone()
    cur.execute("SELECT id, name, roll_no FROM students")
    students = cur.fetchall()
    conn.close()
    if not fee:
        return "Fee record not found!", 404
    return render_template("edit_fee.html", fee=fee, students=students)

# ================ DELETE FEE =================
@app.route("/delete-fee/<int:id>")
def delete_fee(id):
    if 'role' not in session or session['role'] != 'admin':
        return redirect("/admin-login")
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM fees WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return redirect("/fees")
    except Exception as e:
        return f"Error deleting: {e}"

# --------------fee pdf--------------------
@app.route("/student-fees-pdf/<int:id>")
def student_fees_pdf(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    cur.execute("SELECT amount, date, status FROM fees WHERE student_id=?", (id,))
    fees = cur.fetchall()
    conn.close()
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(200, 800, "FEE RECEIPT")
    pdf.drawString(50, 770, f"Student: {student[0]}")
    y = 730
    for f in fees:
        pdf.drawString(50, y, f"{f[1]} | ₹{f[0]} | {f[2]}")
        y -= 20
    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="fee_receipt.pdf", mimetype="application/pdf")

# ---------------Edit-------------------- 
@app.route("/edit-student/<int:id>", methods=["GET","POST"])
def edit_student(id):
    conn = connect_db()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form['name']
        course = request.form['course']
        semester = request.form['semester']
        email = request.form['email']
        phone = request.form['phone']
        cur.execute("UPDATE students SET name=?, course=?, semester=?, email=?, phone=? WHERE id=?", (name, course, semester, email, phone, id))
        conn.commit()
        conn.close()
        return redirect("/students")
    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    conn.close()
    return render_template("edit_student.html", student=student)

# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/students")

# ---------------Student Login---------------
@app.route("/student-login", methods=["GET", "POST"])
def student_login():
    if request.method == "POST":
        roll_no = request.form['roll_no']
        email = request.form['email']
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE roll_no=? AND email=?", (roll_no, email))
        student = cur.fetchone()
        conn.close()
        if student:
            session['role'] = 'student'
            session['student_id'] = student['id']
            session['student_name'] = student['name']
            return redirect("/student-dashboard")
        return "❌ Invalid Login"
    return render_template("student_login.html")

#-----------------Student Dashboard-----------
@app.route("/student-dashboard")
def student_dashboard():
    if 'student_id' not in session:
        return redirect("/student-login")
    sid = session['student_id']
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT subjects.name, attendance.date, attendance.status
        FROM attendance
        JOIN subjects ON subjects.id = attendance.subject_id
        WHERE student_id=?
        ORDER BY attendance.date DESC
        LIMIT 5
    """, (sid,))
    recent = cur.fetchall()
    cur.execute("""
        SELECT subjects.name,
        SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) as present,
        COUNT(*) as total
        FROM attendance
        JOIN subjects ON subjects.id = attendance.subject_id
        WHERE student_id=?
        GROUP BY subjects.name
    """, (sid,))
    subject_data = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?", (sid,))
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'", (sid,))
    present = cur.fetchone()[0]
    percent = round((present/total)*100,2) if total > 0 else 0
    cur.execute("SELECT subject, marks, total FROM marks WHERE student_id=?", (sid,))
    marks = cur.fetchall()
    total_marks = sum([m["marks"] for m in marks]) if marks else 0
    total_max = sum([m["total"] for m in marks]) if marks else 0
    avg_percent = round((total_marks/total_max)*100,2) if total_max > 0 else 0
    conn.close()
    return render_template("student_dashboard.html",
        recent=recent,
        subject_data=subject_data,
        percent=percent,
        marks=marks,
        total_marks=total_marks,
        total_max=total_max,
        avg_percent=avg_percent
    )

@app.route("/student-profile")
def student_profile_page():
    if 'student_id' not in session:
        return redirect("/student-login")
    sid = session['student_id']
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE id=?", (sid,))
    student = cur.fetchone()
    cur.execute("""
        SELECT subjects.name as subject, attendance.date, attendance.status
        FROM attendance
        JOIN subjects ON subjects.id = attendance.subject_id
        WHERE attendance.student_id=?
        ORDER BY attendance.date DESC
    """, (sid,))
    attendance = cur.fetchall()
    cur.execute("SELECT amount, date, status FROM fees WHERE student_id=? ORDER BY date DESC", (sid,))
    fees = cur.fetchall()
    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=?", (sid,))
    total_att = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND status='Present'", (sid,))
    present_att = cur.fetchone()[0] or 0
    attendance_percent = round((present_att / total_att) * 100, 2) if total_att > 0 else 0
    cur.execute("SELECT SUM(marks), SUM(total) FROM marks WHERE student_id=?", (sid,))
    marks_data = cur.fetchone()
    total_marks = marks_data[0] or 0
    total_max = marks_data[1] or 0
    avg_percent = round((total_marks / total_max) * 100, 2) if total_max > 0 else 0
    cur.execute("SELECT SUM(amount) FROM fees WHERE student_id=? AND status='Paid'", (sid,))
    total_fees = cur.fetchone()[0] or 0
    conn.close()
    return render_template("student_profile_page.html",
                          student=student,
                          attendance=attendance,
                          fees=fees,
                          attendance_percent=attendance_percent,
                          avg_percent=avg_percent,
                          total_fees=total_fees)

# -----------------add-marks----------------
@app.route("/add-marks", methods=["GET","POST"])
def add_marks():
    if session.get("role") not in ["admin","teacher"]:
        return redirect("/login")
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if request.method == "POST":
        student_id = request.form.get("student_id")
        subject = request.form.get("subject")
        marks = request.form.get("marks")
        total = request.form.get("total")
        cur.execute("INSERT INTO marks(student_id, subject, marks, total) VALUES (?,?,?,?)", (student_id, subject, marks, total))
        conn.commit()
    cur.execute("SELECT id, name FROM students")
    students = cur.fetchall()
    cur.execute("SELECT marks.id, students.name, marks.subject, marks.marks, marks.total FROM marks JOIN students ON students.id = marks.student_id")
    all_marks = cur.fetchall()
    conn.close()
    return render_template("add_marks.html", students=students, all_marks=all_marks)

# ----------------edit_marks--------------------
@app.route("/edit-marks/<int:id>", methods=["GET","POST"])
def edit_marks(id):
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    if request.method == "POST":
        subject = request.form.get("subject")
        marks = request.form.get("marks")
        total = request.form.get("total")
        cur.execute("UPDATE marks SET subject=?, marks=?, total=? WHERE id=?", (subject, marks, total, id))
        conn.commit()
        return redirect("/add-marks")
    cur.execute("SELECT * FROM marks WHERE id=?", (id,))
    data = cur.fetchone()
    conn.close()
    return render_template("edit_marks.html", m=data)

# -----------------Delete_marks---------------
@app.route("/delete-marks/<int:id>")
def delete_marks(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM marks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/add-marks")

# -----------------student_edit--------------
@app.route("/student-edit", methods=["GET", "POST"])
def student_edit():
    if 'student_id' not in session:
        return redirect("/student-login")
    sid = session['student_id']
    conn = connect_db()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        photo_file = request.files.get('photo')
        filename = None
        if photo_file and photo_file.filename != "":
            filename = secure_filename(photo_file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo_file.save(path)
            cur.execute("UPDATE students SET name=?, email=?, phone=?, photo=? WHERE id=?", (name, email, phone, filename, sid))
        else:
            cur.execute("UPDATE students SET name=?, email=?, phone=? WHERE id=?", (name, email, phone, sid))
        conn.commit()
    cur.execute("SELECT * FROM students WHERE id=?", (sid,))
    student = cur.fetchone()
    conn.close()
    return render_template("student_edit.html", student=student)

# ---------------Teacher login------------
@app.route("/teacher-login", methods=["GET", "POST"])
def teacher_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND role='teacher'", (username,))
        user = cur.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['role'] = 'teacher'
            session['user'] = user['username']
            return redirect("/teacher-dashboard")
        return "❌ Invalid Login"
    return render_template("teacher_login.html")

# ----------------Teacher Dasboard-------------
@app.route("/teacher-dashboard")
def teacher_dashboard():
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attendance")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attendance WHERE status='Present'")
    present = cur.fetchone()[0]
    attendance_percent = 0
    if total > 0:
        attendance_percent = round((present / total) * 100, 2)
    today = date.today()
    cur.execute("SELECT COUNT(*) FROM attendance WHERE date=?", (today,))
    today_total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='Present'", (today,))
    today_present = cur.fetchone()[0]
    today_absent = today_total - today_present
    cur.execute("""
    SELECT attendance.id, students.name, subjects.name, attendance.date, attendance.status
    FROM attendance
    JOIN students ON students.id = attendance.student_id
    JOIN subjects ON subjects.id = attendance.subject_id
    """)
    records = cur.fetchall()
    conn.close()
    return render_template("teacher_dashboard.html",
        total_students=total_students,
        today_present=today_present,
        today_absent=today_absent,
        attendance_percent=attendance_percent,
        records=records
    )

# ---------------- ADMIN LOGIN ----------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=? AND role='admin'", (username,))
        user = cur.fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['role'] = 'admin'
            session['user'] = user['username']
            return redirect("/dashboard")
        return "❌ Invalid Login"
    return render_template("admin_login.html")

# ----------------teacher_student--------------
@app.route("/teacher/students")
def teacher_students():
    if session.get('role') != 'teacher':
        return redirect("/teacher-login")
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    conn.close()
    return render_template("teacher_students.html", students=data)

# === PUBLIC WEBSITE (No Login Required) ===
@app.route("/")
def index():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM subjects")
    total_courses = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students WHERE course='B.Tech'")
    btech_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students WHERE course='MBA'")
    mba_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students WHERE course='BCA'")
    bca_students = cur.fetchone()[0] or 0
    cur.execute("SELECT * FROM notices ORDER BY id DESC LIMIT 3")
    notices = cur.fetchall()
    conn.close()
    return render_template("public_index.html",
        total_students=total_students,
        total_courses=total_courses,
        total_teachers=total_teachers,
        btech_students=btech_students,
        mba_students=mba_students,
        bca_students=bca_students,
        notices=notices
    )

# ================ PUBLIC WEBSITE PAGES ================

@app.route("/")
def public_index():
    """Home Page"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM subjects")
    total_courses = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students WHERE course='B.Tech'")
    btech_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students WHERE course='MBA'")
    mba_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students WHERE course='BCA'")
    bca_students = cur.fetchone()[0] or 0
    cur.execute("SELECT * FROM notices ORDER BY id DESC LIMIT 5")
    notices = cur.fetchall()
    conn.close()
    return render_template("public_index.html",
        total_students=total_students,
        total_courses=total_courses,
        total_teachers=total_teachers,
        btech_students=btech_students,
        mba_students=mba_students,
        bca_students=bca_students,
        notices=notices
    )

@app.route("/about")
def about():
    """About Us Page"""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM teachers")
    total_teachers = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0] or 0
    cur.execute("SELECT COUNT(*) FROM subjects")
    total_courses = cur.fetchone()[0] or 0
    conn.close()
    return render_template("about.html", 
                         total_teachers=total_teachers,
                         total_students=total_students,
                         total_courses=total_courses)

@app.route("/courses")
def courses():
    """Courses Page"""
    conn = connect_db()
    cur = conn.cursor()
    
    # Get all courses with details
    cur.execute("SELECT DISTINCT course FROM students")
    courses_list = cur.fetchall()
    
    # Course wise student count
    course_stats = []
    for course in courses_list:
        cur.execute("SELECT COUNT(*) FROM students WHERE course=?", (course[0],))
        count = cur.fetchone()[0]
        course_stats.append({'name': course[0], 'count': count})
    
    conn.close()
    return render_template("courses.html", courses=course_stats)

@app.route("/admission")
def admission():
    """Admission Page"""
    return render_template("admission.html")

@app.route("/apply", methods=["GET", "POST"])
def apply():
    """Apply Online Page"""
    if request.method == "POST":
        # Get form data
        name = request.form.get('fullName')
        email = request.form.get('email')
        phone = request.form.get('mobile')
        course = request.form.get('course')
        qualification = request.form.get('qualification')
        percentage = request.form.get('percentage')
        passing_year = request.form.get('passingYear')
        address = request.form.get('address')
        
        # Save to database (create applications table if needed)
        conn = connect_db()
        cur = conn.cursor()
        
        # Create applications table if not exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                course TEXT,
                qualification TEXT,
                percentage TEXT,
                passing_year TEXT,
                address TEXT,
                application_date TEXT,
                status TEXT
            )
        """)
        
        from datetime import datetime
        cur.execute("""
            INSERT INTO applications (name, email, phone, course, qualification, percentage, passing_year, address, application_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, course, qualification, percentage, passing_year, address, datetime.now().isoformat(), 'Pending'))
        
        conn.commit()
        conn.close()
        
        # Send confirmation email
        subject = "Application Received - Elite University"
        message = f"""Dear {name},

Thank you for applying to Elite University!

Your application has been received successfully. Our admission team will review your application and contact you within 7 working days.

Application Details:
- Course: {course}
- Qualification: {qualification}
- Percentage: {percentage}%
- Passing Year: {passing_year}

For any queries, please contact our admission helpline: +91 1234567890

Best Regards,
Admission Committee
Elite University"""
        
        send_email(email, subject, message)
        
        return render_template("apply.html", success=True, application_name=name)
    
    return render_template("apply.html", success=False)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """Contact Page"""
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Save to database
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                phone TEXT,
                subject TEXT,
                message TEXT,
                date TEXT
            )
        """)
        
        from datetime import datetime
        cur.execute("""
            INSERT INTO contacts (name, email, phone, subject, message, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, phone, subject, message, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        
        # Send auto-reply
        auto_reply = f"""Dear {name},

Thank you for contacting Elite University!

We have received your message and our team will get back to you within 24 hours.

Your Query: {message}

Best Regards,
Elite University Support Team
www.eliteuniversity.edu"""
        
        send_email(email, "We received your message - Elite University", auto_reply)
        
        return render_template("contact.html", success=True)
    
    return render_template("contact.html", success=False)

# ---------------- LOGOUT -------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/admin-login")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)