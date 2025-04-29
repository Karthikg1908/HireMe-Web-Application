import sqlite3
from flask import jsonify
def register_student(usn, name, email, password, confirmPassword, skills, branch, college_name, phone_number,resume):
    print(name)
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()     
    cursor.execute('SELECT * FROM students WHERE usn = ?',(usn,))
    student = cursor.fetchone()
    if student:
        conn.close()
        return jsonify({'redirected': False, 'message': 'User already exists'})
    else:
        if password == confirmPassword:
            cursor.execute('''INSERT INTO students (usn, student_name, contact_number, college_name, branch, skills, email_id, password, resume)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',(usn,name, phone_number, college_name, branch, skills, email, password, resume))
            conn.commit()
            conn.close()
            return jsonify({'redirected': True, 'url': '/student_login'})
        else:
            return jsonify({'redirected': False, 'message': 'Passwords do not match'})
            
            
            
    
    
