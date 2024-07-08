import MySQLdb
import mysql.connector
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
import os

cnx = mysql.connector.connect(
    user='root',
    password='root',
    host='127.0.0.1'
)

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
            return redirect(url_for('dashboard'))
        else:
            flash('Email/Senha não encontrados', 'error')

    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    userid = session['user_id']
    arquivos = []

    if session['role'] == 'Administrador':
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files")
        arquivos = cur.fetchall()
    elif session['role'] == 'Gerente de departamento':
        cur.execute("SELECT Title, link, Img, Departamento, Empresa FROM files WHERE Departamento = %s AND Empresa = %s",
                    (session['departamento'], session['empresa']))
        arquivos = cur.fetchall()
    elif session['role'] == 'Gestor':
        cur.execute("SELECT idfiles FROM filesusers WHERE idusers = %s", (userid,))
        dash = cur.fetchall()

        idfiles_list = [item[0] for item in dash]
        if idfiles_list:
            placeholders = ', '.join(['%s'] * len(idfiles_list))
            query = f"SELECT Title, link, Img, Departamento, Empresa FROM files WHERE idfiles IN ({placeholders})"
            cur.execute(query, idfiles_list)
            arquivos = cur.fetchall()
    else:
        cur.execute("SELECT idfiles FROM filesusers WHERE idusers = %s", (userid,))
        dash = cur.fetchall()

        idfiles_list = [item[0] for item in dash]
        if idfiles_list:
            placeholders = ', '.join(['%s'] * len(idfiles_list))
            query = f"SELECT Title, link, Img, Departamento, Empresa FROM files WHERE idfiles IN ({placeholders})"
            cur.execute(query, idfiles_list)
            arquivos = cur.fetchall()

    # Agrupa arquivos por departamento
    arquivos_por_departamento = {}
    for arquivo in arquivos:
        departamento = arquivo[3]  # índice do campo 'Departamento'
        if departamento not in arquivos_por_departamento:
            arquivos_por_departamento[departamento] = []
        arquivos_por_departamento[departamento].append(arquivo)

    # Obter nomes dos departamentos
    departamentos = list(arquivos_por_departamento.keys())
    placeholders = ', '.join(['%s'] * len(departamentos))
    query = f"SELECT nome FROM departamentos WHERE nome IN ({placeholders})"
    cur.execute(query, departamentos)
    departamento_name = cur.fetchall()

    cur.close()

    return render_template('dashboard.html', arquivos_por_departamento=arquivos_por_departamento, departamento_name=departamento_name)

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

    return redirect(url_for('dashboard'))


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

    departamento = session['departamento']
    empresa = session['empresa']

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['role'] == 'Administrador':
        cursor.execute('SELECT * FROM users')
    elif session['role'] == 'Gestor':
        cursor.execute('SELECT * FROM users WHERE company = %s', (empresa, ))
    elif session['role'] == 'Gerente de departamento':
        cursor.execute('SELECT * FROM users WHERE company = %s and departament =%s ', (empresa, departamento,))

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
        cur.execute(
            "INSERT INTO users (username, email, password, company, departament, role) VALUES (%s, %s, %s, %s, %s, %s)",
            (username, email, password, company, departament, role))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('CadastrarUser'))

    return render_template('cadastrar_usuario.html', titulo='cadastrarUser')


@app.route('/CadastrarDashboard', methods=['GET', 'POST'])
def CadastrarDashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        image = request.form['img']
        company = request.form['company']
        department = request.form['department']
        selected_users = request.form.getlist('usuario')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO files (title, link, img, empresa, departamento) VALUES (%s, %s, %s, %s, %s)",
                    (title, link, image, company, department))
        mysql.connection.commit()

        file_id = cur.lastrowid

        for usuario_id in selected_users:
            cur.execute('''INSERT INTO filesusers (idfiles, idusers) VALUES (%s, %s)''',(file_id, usuario_id))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('CadastrarDashboard'))

    department = session['departamento']
    company = session['empresa']

    if session['role'] == 'Gerente de departamento':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE departament = %s AND company = %s",
                       (department, company))
    elif session['role'] == 'Gestor':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE company = %s",
                       (company,))
    elif session['role'] == 'Administrador':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users")

    usuarios = cursor.fetchall()

    return render_template('cadastrar_dashboard.html', titulo='cadastrarDashboard', usuarios=usuarios)


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


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        empresa = request.form['company']
        departamento = request.form['departament']
        role = request.form['role']

        # Atualiza os dados do usuário no banco de dados
        cur.execute("""
            UPDATE users
            SET username = %s, email = %s, company = %s, departament = %s, role = %s
            WHERE idusers = %s
        """, (nome, email, empresa, departamento, role, id))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('config'))

    # Obtém os dados atuais do usuário para preencher o formulário
    cur.execute("SELECT * FROM users WHERE idusers = %s", (id,))
    usuario = cur.fetchone()
    cur.close()

    return render_template('editar_usuario.html', usuario=usuario)


if __name__ == '__main__':
    app.run(debug=True)
