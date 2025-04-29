import sqlite3

def get_jobs_by_application_status(usn):
    with sqlite3.connect('db/hireme.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT jobs.*, 
                   CASE 
                       WHEN student_applications.job_id IS NOT NULL THEN 'applied' 
                       ELSE 'not applied' 
                   END AS status 
            FROM jobs 
            LEFT JOIN student_applications 
              ON jobs.id = student_applications.job_id AND student_applications.usn = ?
            WHERE jobs.status != 'closed'
        ''', (usn,))
        jobs = cursor.fetchall()

    categorized_jobs = {  
        "not_applied": [dict(id=job[0], job_role=job[1], company=job[2], package=job[3], job_description=job[4]) 
                        for job in jobs if job[-1] == 'not applied'],  
        "applied": [dict(id=job[0], job_role=job[1], company=job[2], package=job[3], job_description=job[4]) 
                    for job in jobs if job[-1] == 'applied']  
    }  
    return categorized_jobs

def apply_job(usn, job_id):
    with sqlite3.connect('db/hireme.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student_applications WHERE usn = ? AND job_id = ?', (usn, job_id))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO student_applications (usn, job_id) VALUES (?, ?)', (usn, job_id))
            conn.commit()
            return True  # Successfully applied
        else:
            return False  # Already applied

def fetch_job_details(job_id):
    with sqlite3.connect('db/hireme.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        job = cursor.fetchone()
    
    if job:
        return {
            "job_role": job[1], 
            "company": job[2],
            "package": job[3],
            "job_description": job[4]
        }
    else:
        return None

def remove_application(usn, job_id):
    with sqlite3.connect('db/hireme.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM student_applications WHERE usn = ? AND job_id = ?', (usn, job_id))
        conn.commit()
        return cursor.rowcount > 0  # Returns True if something was deleted

