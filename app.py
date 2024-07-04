import MySQLdb
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
            flash('Email/Senha não encontrados','error')

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    if session['role'] == 'Administrador':
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files")
    else:
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = %s", (session['departamento'],))

    arquivos = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', arquivos=arquivos, titulo=dashboard)


# <---HOME--->
@app.route('/home')
def home():
    if 'user_id' not in session or session['user_id'] is None:
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

    return render_template('home.html', arquivos=arquivos, titulo='home')


# <---LOGOUT--->
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


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

@app.route('/cadastrarUser', methods=['POST'])
def cadastrarUser():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    nome = request.form['Nome']
    email = request.form['email']
    nível = request.files['nivel']
    empresa = request.files['empresa']
    departamento = request.files['departamento']
    senha = request.files['senha']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username, email, role, company, departament, password) VALUES (%s, %s, %s)",
                (nome, email, nível, empresa, departamento, senha))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('config'))

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

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    usuarios = cursor.fetchall()

    return render_template('config.html', arquivos=arquivos, usuarios=usuarios, titulo='config')


@app.route('/CadastrarUser', methods=['GET', 'POST'])
def CadastrarUser():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        company = request.form['company']
        departament = request.form['departament']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password, company, departament, role) VALUES (%s, %s, %s, %s, %s, %s)",(username, email, password, company, departament, role))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('CadastrarUser'))

    return render_template('cadastrar_usuario.html', titulo='cadastrarUser')


@app.route('/excluir/<int:usuario_id>', methods=['POST'])
def excluirUsuario(usuario_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE idusers = %s", (usuario_id,))
    mysql.connection.commit()
    cur.close()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('config'))

if __name__ == '__main__':
    app.run(debug=True)