import sqlite3
from flask import  session
def generate_report():
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()

    jobsdata = cursor.execute('SELECT * FROM jobs where rec_id = ?', (session['rec_id'],)).fetchall()
    appliedData = cursor.execute('SELECT * FROM student_applications').fetchall()
    studentData = cursor.execute('SELECT * FROM students').fetchall()

    conn.close()

    report_data = []

    for app in appliedData:
        student = next((s for s in studentData if s[0] == app[1]), None)
        job = next((j for j in jobsdata if j[0] == app[2]), None)

        if student and job:
            report_data.append({
                'application_id': app[0],
                'student_name': student[1],
                'branch': student[4],
                'email_id': student[6],       # 👈 Added this line
                'college': student[3],
                'job_role': job[1],
                'company': job[2],
                'package': job[3],
                'status': app[3],
                'resume':student[8], # 👈 Added this line
                'action':app[4],
            })

    return report_data

