import sqlite3
from flask import session
def add_job(job_role, company, package, job_description):
    conn2 = sqlite3.connect('db/hireme.db')
    cursor2 = conn2.cursor()
    cursor2.execute('''INSERT INTO jobs (job_role, company, package, job_description,rec_id)VALUES (?, ?, ?, ?,?)''', (job_role, company, package, job_description,session['rec_id']))
    conn2.commit()
    conn2.close()
    
    