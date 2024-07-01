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
        cur.execute(
            "SELECT idusers, username, email, password, role, company, departament FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()
        cur.close()

        if email and password == user[3]:
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['email'] = email[2]
            session['departamento'] = user[6]
            session['empresa'] = user[5]
            session['role'] = user[4]
            return redirect(url_for('home'))
        else:
            flash('Invalid login credentials')

    return render_template('index.html')


# <---DASHBOARD--->
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    dep = session['departamento']
    print(dep)

    cur = mysql.connection.cursor()
    if session['role'] == 'Administrador':
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files")
    else:
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = %s", (dep,))

    arquivos = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', arquivos=arquivos)


# <---HOME--->
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    if session['role'] == 'Administrador':
        cur.execute("SELECT Nome, Imagem, link FROM departamentos")
    else:
        cur.execute(
            "SELECT Nome, Imagem, link FROM departamentos WHERE Nome = %s",
            (session['departamento'],)
        )

    arquivos = cur.fetchall()
    cur.close()

    print(arquivos)

    return render_template('home.html', arquivos=arquivos)


# <---LOGOUT--->
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# <---REGISTER NEW FILE--->
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


# <---REGISTER NEW DEPARTAMENT--->
@app.route('/cadastrarDep', methods=['POST'])
def cadastrarDep():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Nome = request.form['Nome']
    link = request.form['Link']
    Imagem = request.files['Imagem']

    img_filename = Imagem.filename
    Imagem.save(os.path.join('static/img', img_filename))

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Departamentos (Nome, Imagem, link) VALUES (%s, %s, %s)",
                (Nome, img_filename, link))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home'))


@app.route('/cadastrarFile', methods=['POST'])
def cadastrarFile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Nome = request.form['Nome']
    link = request.form['Link']
    Imagem = request.files['Imagem']
    departamento = request.form['Departamento']
    empresa = request.form['Empresa']

    img_filename = Imagem.filename
    Imagem.save(os.path.join('static/img/dash', img_filename))

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO files (Title, img, link, departamento, empresa) VALUES (%s, %s, %s, %s, %s)",
                (Nome, img_filename, link, departamento, empresa))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('dashboard'))


@app.route('/config')
def config():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    if session['role'] == 'Administrador':
        cur.execute("SELECT Nome, Imagem, link FROM departamentos")
    else:
        cur.execute(
            "SELECT Nome, Imagem, link FROM departamentos WHERE Nome = %s",
            (session['departamento'],)
        )

    arquivos = cur.fetchall()
    cur.close()

    return render_template('config.html', arquivos=arquivos)


if __name__ == '__main__':
    app.run(debug=True)
