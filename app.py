from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from database import init_db
from pythonfiles.report import generate_report
from pythonfiles.Student_reset_pass import update_student_password
from pythonfiles.rec_forgotpassword import update_password
from pythonfiles.recruiter_register import register_recruiter
from pythonfiles.create_job import add_job
from pythonfiles.recruiter_home import get_all_jobs
from pythonfiles.Student_home import apply_job, fetch_job_details, get_jobs_by_application_status
from pythonfiles.recruiterslogin import *
from pythonfiles.students_login import *
from pythonfiles.Students_register import register_student
from flask_cors import CORS
from reportlab.pdfgen import canvas
from flask import send_file
from flask import Flask, render_template, request, redirect, session, url_for, flash
import os

app = Flask(__name__)
app.secret_key = '2345'
CORS(app)

# Initialize the database
init_db()

# Route for index page
@app.route('/')
def index():
    return render_template('index.html') 


# ++++++++++++++++++++++++++++++++++++++ START OF STUDENT REGISTRATION +++++++++++++++++++++++++++++++
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/student_register', methods=['POST'])
def student_register():
    resume = request.files['resume']
    filename = secure_filename(resume.filename)
    resume.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Collect other form data
    usn = request.form['usn']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirmPassword = request.form['confirm_password']
    skills = request.form['skills']
    branch = request.form['branch']
    college_name = request.form['college_name']
    phone_number = request.form['phone_number']

    return register_student(usn, name, email, password, confirmPassword, skills, branch, college_name, phone_number, filename)

@app.route('/student_register')
def student_register_page():
    return render_template('student_register.html')  

# ++++++++++++++++++++++++++++++++++++++ END OF STUDENT REGISTRATION ++++++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF RECRUITER REGISTRATION +++++++++++++++++++++++++++++

@app.route("/recruiter_register", methods=['POST'])
def recruiter_register():
    data = request.get_json()
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    confirmPassword = data.get('confirm_password')
    company = data.get('company')
    phone_number = data.get('phone_number')
    return register_recruiter(username, firstname, lastname, email, password, confirmPassword, company, phone_number)
    
@app.route('/recruiter_register')
def recruiter_register_page():
    return render_template('recruiter_register.html')
    

# ++++++++++++++++++++++++++++++++++++++ END OF RECRUITER REGISTRATION ++++++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ CREATE JOB PAGE ++++++++++++++++++++++++++

@app.route('/api/jobs', methods=['POST'])
def api_add_job():
    data = request.get_json()
    job_role = data.get('job_role')
    company = data.get('company')
    package = data.get('package')
    job_description = data.get('job_description')
    add_job(job_role, company, package, job_description)
    return jsonify({'success': True})
    
@app.route('/create_job_page')
def create_job_page():
    return render_template('create_job.html')
    
@app.route('/api/job', methods=['POST'])
def create_job_alias():
    return create_job()

@app.route('/api/job/<int:job_id>', methods=['GET', 'PUT'])
def job_detail(job_id):
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            job = {
                'id': row[0],
                'job_role': row[1],
                'company': row[2],
                'package': row[3],
                'job_description': row[4]
            }
            return jsonify(job)
        return jsonify({'error': 'Job not found'}), 404

    elif request.method == 'PUT':
        data = request.get_json()
        cursor.execute('''
            UPDATE jobs SET job_role = ?, company = ?, package = ?, job_description = ?
            WHERE id = ?
        ''', (
            data['job_role'], data['company'], data['package'], data['job_description'], job_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})

# +++++++++++++++++++++++++++ END OF CREATE JOB PAGE ++++++++++++++++++++++++++

# +++++++++++++++++++++++++++ START OF RECRUITER LOGIN ++++++++++++++++++++++++++

@app.route('/recruiter_login', methods=['POST'])
def recruiter_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return check_recruiter_login(username, password)
    
@app.route('/recruiter_login')
def recruiter_login_page():
    return render_template('recruiter_login.html')
    

# +++++++++++++++++++++++++++ END OF RECRUITER LOGIN ++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ RECRUITER HOME PAGE ++++++++++++++++++++++++++++++

@app.route('/recruiter_home')
def recruiter_home():
    return render_template('recruiter_home.html')
    
@app.route('/recruiter/job/<int:job_id>')
def recruiter_job_page(job_id):
    return render_template('recruiter_job_details.html')
    
@app.route('/api/job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
    conn.commit()
    conn.close()
    return '', 204  # 204 No Content

@app.route('/api/jobs', methods=['GET'])
def api_get_jobs():
    if 'rec_id' not in session:
        return jsonify([])  # or handle as unauthorized
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, job_role, company, package, status FROM jobs WHERE rec_id = ?', (session['rec_id'],))
    jobs = cursor.fetchall()
    conn.close()
    return jsonify(jobs)

# Route to fetch a single job for editing
@app.route('/api/job/<int:job_id>', methods=['GET'])
def get_job(job_id):
    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
    job = cursor.fetchone()
    conn.close()
    if job:
        return jsonify({
            'job_role': job[1],
            'company': job[2],
            'package': job[3],
            'job_description': job[4]
        })
    else:
        return jsonify({'error': 'Job not found'}), 404

# Route to update an existing job
@app.route('/api/job/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    data = request.get_json()
    job_role = data.get('job_role')
    company = data.get('company')
    package = data.get('package')
    job_description = data.get('job_description')

    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE jobs SET job_role = ?, company = ?, package = ?, job_description = ? WHERE id = ?',
                   (job_role, company, package, job_description, job_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

# Route to update job status (open/closed)
@app.route('/api/job/<int:job_id>/status', methods=['PUT'])
def update_job_status(job_id):
    data = request.get_json()
    new_status = data.get('status')

    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET status = ? WHERE id = ?", (new_status, job_id))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

# Route to create a new job (POST remains the same)
@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    job_role = data.get('job_role')
    company = data.get('company')
    package = data.get('package')
    job_description = data.get('job_description')

    conn = sqlite3.connect('db/hireme.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO jobs (job_role, company, package, job_description, status,rec_id) VALUES (?, ?, ?, ?, ?,?)',
                   (job_role, company, package, job_description, 'open',session['rec_id']))
    conn.commit()
    conn.close()

    return jsonify({'success': True})

# ++++++++++++++++++++++++++++++++++++++ END OF RECRUITER HOME PAGE ++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++++++ START OF STUDENT LOGIN +++++++++++++++++++++++++++++

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usn = data.get('usn')
    password = data.get('password')
    return check_student_login(usn, password)
    
@app.route('/student_login')
def student_login():
    return render_template('student_login.html')
    

# ++++++++++++++++++++++++++++++++++++++ END OF STUDENT LOGIN +++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF STUDENT HOME PAGE +++++++++++++++++++++++++++++

@app.route('/api/apply_job', methods=['POST'])

def apply_job_route():
    data = request.get_json()
    usn1 = session.get('usn')
    job_id = data.get('job_id')
    apply_job(usn1, job_id)
    return jsonify({'success': True})
    
@app.route('/student_home')
def student_home():
    return render_template('student_home.html')

@app.route('/api/jobs_by_status', methods=['GET'])
def api_get_jobs_by_status():
    usn2 = session.get('usn')
    if not usn2:
        return jsonify({'error': 'Unauthorized'}), 401
    categorized_jobs = get_jobs_by_application_status(usn2)
    return jsonify(categorized_jobs) 
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/job_details/<int:job_id>')
def job_details(job_id):
    job = fetch_job_details(job_id)
    if job:
        return jsonify(job)
    else:
        return jsonify({'error': 'Job not found'}), 404 
        
@app.route('/api/withdraw_application', methods=['POST'])
def withdraw_application():
    data = request.get_json()
    job_id = data.get('job_id')
    usn = session.get('usn')  # or fetch from localStorage if passed via frontend
    if not usn or not job_id:
        return jsonify({'success': False, 'error': 'Missing data'})

    success = remove_application(usn, job_id)
    return jsonify({'success': success})
def remove_application(usn, job_id):
    with sqlite3.connect('db/hireme.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM student_applications WHERE usn = ? AND job_id = ?', (usn, job_id))
        conn.commit()
        return cursor.rowcount > 0  # Returns True if something was deleted

# ++++++++++++++++++++++++++++++++++++++ END OF STUDENT HOME PAGE +++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF JOB DETAILS +++++++++++++++++++++++++++++

@app.route('/job/<int:job_id>')
def job_page(job_id):
    return render_template('job_details.html')
    

# ++++++++++++++++++++++++++++++++++++++ END OF JOB DETAILS +++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF RECRUITER FORGOT PASSWORD +++++++++++++++++++++++++++++

@app.route('/rec_forgot_password')
def forgot_password_page():
     return render_template('rec_forgot_password.html')
     
@app.route("/forgot_password", methods=['POST'])
def  forgot_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    if new_password != confirm_password:
        return jsonify({'success': False, 'message': 'Passwords do not match'})
    return update_password(username, new_password)
        
    
    
# ++++++++++++++++++++++++++++++++++++++ END OF RECRUITER FORGOT PASSWORD ++++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF STUDENT FORGOT PASSWORD +++++++++++++++++++++++++++++

@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    usn = data.get('usn')
    email = data.get('email')
    new_password = data.get('new_password')

    if not usn or not email or not new_password:
        return jsonify({'success': False, 'message': 'Please fill all the fields'}), 400

    return update_student_password(usn, email, new_password)

# Route to serve the password reset page
@app.route('/reset-password-page')
def reset_password_page():
    return render_template('student_reset_password.html')



# ++++++++++++++++++++++++++++++++++++++ END OF STUDENT FORGOT PASSWORD +++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF REPORT PAGE +++++++++++++++++++++++++++++

@app.route('/report')
def report_page():
    return render_template('report.html')

@app.route('/api/report')
def api_report_data():
    report_data = generate_report()
    return jsonify(report_data)

from flask import send_from_directory
@app.route('/resumes/<filename>')
def serve_resume(filename):
    return send_from_directory('uploads', filename)

@app.route('/api/update_action', methods=['POST'])
def update_action():
    data = request.get_json()
    application_id = data.get('application_id')
    action = data.get('action')

    if not application_id or not action:
        return jsonify({'error': 'Missing application_id or action'}), 400

    conn = sqlite3.connect('db/hireme.db')  # adjust path if needed
    cursor = conn.cursor()

    cursor.execute("UPDATE student_applications SET action = ? WHERE id = ?", (action, application_id))
    conn.commit()
    conn.close()

    return jsonify({'message': f"Action updated to '{action}' for application_id {application_id}"}), 200




# ++++++++++++++++++++++++++++++++++++++ END OF REPORT PAGE +++++++++++++++++++++++++++++

# ++++++++++++++++++++++++++++++++++++++ START OF EDIT STUDENT PROFILE PAGE +++++++++++++++++++++++++++++

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'usn' not in session:
        return redirect('/student_login')

    usn = session['usn']
    conn = sqlite3.connect('db/hireme.db', check_same_thread=False)
    cursor = conn.cursor()

    try:
        if request.method == 'POST':
            student_name = request.form.get('name')
            email_id = request.form.get('email')
            contact_number = request.form.get('phone')
            skills = request.form.get('skills')
            branch = request.form.get('branch')
            college_name = request.form.get('college_name')
            new_password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Check if password fields match
            if new_password != confirm_password:
                return """
                    <script>
                        alert("Passwords do not match. Please try again.");
                        window.location.href = "/edit_profile";
                    </script>
                """

            # Update student information (including password if provided)
            if new_password:
                cursor.execute('''
                    UPDATE students 
                    SET student_name=?, email_id=?, contact_number=?, skills=?, branch=?, college_name=?, password=? 
                    WHERE usn=?
                ''', (student_name, email_id, contact_number, skills, branch, college_name, new_password, usn))
            else:
                # No password change, just update other fields
                cursor.execute('''
                    UPDATE students 
                    SET student_name=?, email_id=?, contact_number=?, skills=?, branch=?, college_name=? 
                    WHERE usn=?
                ''', (student_name, email_id, contact_number, skills, branch, college_name, usn))
                
            conn.commit()

            # Show alert and redirect using JavaScript
            return """
                <script>
                    alert("Profile updated successfully!");
                    window.location.href = "/student_home";
                </script>
            """

        cursor.execute('''
            SELECT student_name, email_id, usn, contact_number, skills, branch, college_name 
            FROM students WHERE usn=?
        ''', (usn,))
        student = cursor.fetchone()

    except sqlite3.OperationalError as e:
        print("Database error:", e)
        return "An error occurred while accessing the database."

    finally:
        conn.close()

    if student:
        return render_template('edit_profile.html', student={
            'name': student[0],
            'email': student[1],
            'usn': student[2],
            'phone_number': student[3],
            'skills': student[4],
            'branch': student[5],
            'college_name': student[6]
        })
    else:
        return "Student not found"


# ++++++++++++++++++++++++++++++++++++++ END OF STUDENT PROFILE PAGE +++++++++++++++++++++++++++++


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port,debug=True)