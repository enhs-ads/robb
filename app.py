from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session security

# Create database and table if not exist
def init_db():
    conn = sqlite3.connect('database1.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = username
            return f'✅ Logged in as {username}'
        else:
            msg = '❌ Invalid username or password'
    return render_template('login1.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database1.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            msg = 'An error accured in the server'
        except sqlite3.IntegrityError:
            msg = '❌ Username already taken.'
        conn.close()
    return render_template('register.html', msg=msg)

@app.route('/show-users')
def show_users():
    conn = sqlite3.connect('database1.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()

    result = "<h2>Registered Users</h2>"
    for user in users:
        result += f"ID: {user[0]} | Username: {user[1]} | Password: {user[2]}<br>"
    return result


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
