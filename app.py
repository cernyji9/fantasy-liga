from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Připojení k databázi
def init_db():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                          )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS teams (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            player_name TEXT,
                            FOREIGN KEY(user_id) REFERENCES users(id)
                          )''')

init_db()

# Hlavní stránka
@app.route('/')
def index():
    return render_template('index.html')

# Registrace uživatele
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Uživatel již existuje!"
    return render_template('register.html')

# Přihlášení uživatele
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            if user:
                return redirect(url_for('team'))
            else:
                return "Nesprávné přihlašovací údaje!"
    return render_template('login.html')

# Stránka s týmem
@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)