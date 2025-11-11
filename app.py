from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)

# Create database if not exists
def init_db():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            contact TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Run init_db when app starts ---
@app.before_first_request
def initialize_database():
    if not os.path.exists('patients.db'):
        init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    patients = c.fetchall()
    conn.close()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']

        conn = sqlite3.connect('patients.db')
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, gender, contact) VALUES (?, ?, ?, ?)",
                  (name, age, gender, contact))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add_patient.html')

@app.route('/delete/<int:id>')
def delete_patient(id):
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute("DELETE FROM patients WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
