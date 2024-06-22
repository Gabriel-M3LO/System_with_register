import app
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
import os

app = Flask(__name__)
app.config.from_object('config.Config')

mysql = MySQL(app)
Session(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT idusers, password, departamento, empresa, role, name FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and password == user[1]:
            session['user_id'] = user[0]
            session['email'] = email
            session['departamento'] = user[2]
            session['empresa'] = user[3]
            session['role'] = user[4]
            session['name'] = user[5]
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials')

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    if session['role'] == 'general':
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files")
    else:
        cur.execute(
            "SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = %s AND Empresa = %s",
            (session['departamento'], session['empresa']))

    arquivos = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', arquivos=arquivos)

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    if session['role'] == 'general':
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files")
    else:
        cur.execute(
            "SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = %s AND Empresa = %s",
            (session['departamento'], session['empresa']))

    arquivos = cur.fetchall()
    cur.close()

    return render_template('home.html', arquivos=arquivos)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    title = request.form['title']
    link = request.form['link']
    departamento = request.form['departamento']
    empresa = request.form['empresa']
    img = request.files['img']

    img_filename = img.filename
    img.save(os.path.join('static/img', img_filename))

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO files (Title, link, Img, Departamento, Empresa) VALUES (%s, %s, %s, %s, %s)",
                (title, link, img_filename, departamento, empresa))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
