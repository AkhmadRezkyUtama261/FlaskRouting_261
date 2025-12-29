from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

# Fungsi untuk membuat database dan tabel jika belum ada
def init_db():
    conn = sqlite3.connect('logins.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logins (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Panggil init_db saat aplikasi start
init_db()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        if name:  # Pastikan nama tidak kosong
            # Simpan ke database
            conn = sqlite3.connect('logins.db')
            c = conn.cursor()
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            c.execute('INSERT INTO logins (name, timestamp) VALUES (?, ?)', (name, timestamp))
            conn.commit()
            conn.close()
            # Redirect ke halaman welcome dengan nama
            return redirect(url_for('welcome', user_name=name))
    return render_template('index.html')

@app.route('/welcome/<user_name>')
def welcome(user_name):
    # Ambil riwayat dari database
    conn = sqlite3.connect('logins.db')
    c = conn.cursor()
    c.execute('SELECT name, timestamp FROM logins ORDER BY timestamp DESC')
    history = c.fetchall()
    conn.close()
    return render_template('index2.html', user_name=user_name, history=history)

if __name__ == '__main__':
    app.run(debug=True)