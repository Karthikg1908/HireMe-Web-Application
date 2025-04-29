import sqlite3
from flask import  session
def get_all_jobs():
    conn1 = sqlite3.connect('db/hireme.db')
    cursor1 = conn1.cursor()
    cursor1.execute('SELECT * FROM jobs where rec_id = ?', (session['rec_id'],))
    jobs = cursor1.fetchall()
    conn1.close()
    return jobs
    