
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            department TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name'].strip()
        roll_no = request.form['roll_no'].strip()
        department = request.form['department'].strip()

        if name and roll_no and department:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO students (name, roll_no, department) VALUES (?, ?, ?)',
                (name, roll_no, department)
            )
            conn.commit()
            conn.close()

        return redirect('/')

    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()

    return render_template('index.html', students=students)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
