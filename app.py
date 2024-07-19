import mail
from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.secret_key = 'root'


app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='Gabrielm3l0',
        senha='nikgeo369',
        servidor='Gabrielm3l0.mysql.pythonanywhere-services.com',
        database='Gabrielm3l0$gestao_correta'
    )

"""
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='root',
        servidor='localhost',
        database='gestao_correta'
    )
"""

app.config['MAIL_SERVER'] = 'smtp-relay.gmail.com'
app.config['MAIL_PORT'] = 4
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'genoreply4@gmail.com'
app.config['MAIL_PASSWORD'] = 'tebn zvkw jcmq jedb'
app.config['MAIL_DEFAULT_SENDER'] = 'genoreply4@gmail.com'


db = SQLAlchemy(app)
mail = Mail(app)

class users(db.Model):
    idusers = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    departament = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Usuario {}>'.format(self.username)


class files(db.Model):
    idFiles = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(80), nullable=False)
    fileImage = db.Column(db.String(80), nullable=False)
    fileDepartment = db.Column(db.String(80), nullable=False)
    fileCompany = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Arquivo {}>'.format(self.title)

# Tabela de associação
files_users = db.Table('filesusers',
    db.Column('idfiles', db.Integer, db.ForeignKey('files.idFiles'), primary_key=True),
    db.Column('idusers', db.Integer, db.ForeignKey('users.idusers'), primary_key=True)
)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = users.query.filter_by(email=request.form['email']).first()
    if usuario:
        if usuario.password == request.form['password']:
            session['usuario_logado'] = usuario.username
            session['departament'] = usuario.departament
            session['username'] = usuario.username
            session['company'] = usuario.company
            session['role'] = usuario.role
            return redirect(url_for('dashboard'))

    return render_template('index.html')

@app.route('/RecuperarSenha', methods=['GET', 'POST'])
def RecuperarSenha():
    if request.method == 'POST':
        try:
            msg = Message(
                'Hello',
                sender='genoreply4@gmail.com',
                recipients=['gabrielzulifi@gmail.com']
            )
            msg.body = 'Hello Flask message sent from Flask-Mail'
            mail.send(msg)
            flash('E-mail enviado com sucesso!', 'success')
        except Exception as e:
            flash(f'Ocorreu um erro ao enviar o e-mail: {str(e)}', 'danger')
        return render_template('RecuperarSenha.html')

    return render_template('RecuperarSenha.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_logado' in session:
        if session['role'] == 'Administrador':
            arquivos = files.query.all()
            print(arquivos)
        elif session['role'] == 'Gerente de departamento':
            arquivos = files.query.filter_by(fileDepartment=session['departament'], fileCompany=session['company']).all()
        elif session['role'] == 'Gestor':
            user_id = users.query.filter_by(username=session['usuario_logado']).first().idusers
            arquivos = db.session.query(files).join(filesusers).filter(filesusers.idusers == user_id).all()
        else:
            user_id = users.query.filter_by(username=session['usuario_logado']).first().idusers
            arquivos = db.session.query(files).join(files_users).join(users).filter(files_users.c.idusers == user_id).all()

        arquivos_por_departamento = {}
        for arquivo in arquivos:
            departamento = arquivo.fileDepartment
            if departamento not in arquivos_por_departamento:
                arquivos_por_departamento[departamento] = []
            arquivos_por_departamento[departamento].append(arquivo)

        departamentos = list(arquivos_por_departamento.keys())
        if departamentos:
            departamento_name = files.query.filter(files.title.in_(departamentos)).all()
        else:
            departamento_name = []

        return render_template('dashboard.html', arquivos_por_departamento=arquivos_por_departamento, departamento_name=departamento_name)
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/cadastrarDep', methods=['POST'])
def cadastrarDep():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    Nome = request.form['Nome']
    link = request.form['Link']
    Imagem = request.files['Imagem']

    img_filename = Imagem.filename
    Imagem.save(os.path.join('static/img', img_filename))

    novo_arquivo = files(title=Nome, link=link, fileImage=img_filename, fileDepartment=session['departament'], fileCompany=session['company'])
    db.session.add(novo_arquivo)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/cadastrarUser', methods=['POST'])
def cadastrarUser():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    nome = request.form['Nome']
    email = request.form['email']
    nível = request.form['nivel']
    empresa = request.form['empresa']
    departamento = request.form['departamento']
    senha = request.form['senha']

    novo_usuario = users(username=nome, email=email, role=nível, company=empresa, departament=departamento, password=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('config'))

@app.route('/cadastrarFile', methods=['POST'])
def cadastrarFile():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    Nome = request.form['Nome']
    link = request.form['Link']
    Imagem = request.files['Imagem']
    departamento = request.form['Departamento']
    empresa = request.form['Empresa']

    img_filename = Imagem.filename
    Imagem.save(os.path.join('static/img/dash', img_filename))

    novo_arquivo = files(title=Nome, link=link, fileImage=img_filename, fileDepartment=departamento, fileCompany=empresa)
    db.session.add(novo_arquivo)
    db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/config')
def config():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    if session['role'] == 'Administrador':
        arquivos = files.query.all()
    else:
        arquivos = files.query.filter_by(fileDepartment=session['departament'], fileCompany=session['company']).all()

    # Definindo 'usuarios' como lista vazia como padrão
    usuarios = []

    if session['role'] == 'Administrador':
        usuarios = users.query.all()
    elif session['role'] == 'Gestor':
        usuarios = users.query.filter_by(company=session['company']).all()
    elif session['role'] == 'Gerente de departamento':
        usuarios = users.query.filter_by(company=session['company'], departament=session['departament']).all()

    # Buscar dashboards
    dashboards = files.query.all()

    return render_template('config.html',dashboards=dashboards, arquivos=arquivos, usuarios=usuarios, titulo='config')


@app.route('/CadastrarUser', methods=['GET', 'POST'])
def CadastrarUser():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        company = request.form['company']
        departament = request.form['departament']
        role = request.form['role']

        novo_usuario = users(username=username, email=email, password=password, company=company, departament=departament, role=role)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('CadastrarUser'))

    return render_template('cadastrar_usuario.html', titulo='cadastrarUser')


@app.route('/CadastrarDashboard', methods=['GET', 'POST'])
def CadastrarDashboard():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        image = request.form['img']
        company = request.form['company']
        department = request.form['department']
        selected_users = request.form.getlist('usuario')

        novo_arquivo = files(title=title, link=link, fileImage=image, fileDepartment=department, fileCompany=company)
        db.session.add(novo_arquivo)
        db.session.commit()

        file_id = novo_arquivo.idFiles

        for usuario_id in selected_users:
            association = filesusers(idfiles=file_id, idusers=usuario_id)
            db.session.add(association)
        db.session.commit()

        return redirect(url_for('CadastrarDashboard'))

    usuarios = []
    if session['role'] == 'Gerente de departamento':
        usuarios = users.query.filter_by(departament=session['departament'], company=session['company']).all()
    elif session['role'] == 'Gestor':
        usuarios = users.query.filter_by(company=session['company']).all()
    elif session['role'] == 'Administrador':
        usuarios = users.query.all()

    return render_template('cadastrar_dashboard.html', titulo='cadastrarDashboard', usuarios=usuarios)


@app.route('/excluir/<int:usuario_id>', methods=['POST'])
def excluirUsuario(usuario_id):
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    usuario = users.query.get(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('config'))


@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = users.query.get(id)

    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.email = request.form['email']
        usuario.company = request.form['company']
        usuario.departament = request.form['departament']
        usuario.role = request.form['role']

        db.session.commit()

        return redirect(url_for('config'))

    return render_template('editar_usuario.html', usuario=usuario)


@app.route('/editar_dashboard/<int:id>', methods=['GET', 'POST'])
def editar_dashboard(id):
    dashboard = files.query.get_or_404(id)

    if request.method == 'POST':
        dashboard.title = request.form['title']
        dashboard.link = request.form['link']
        dashboard.fileImage = request.form['fileImage']
        dashboard.fileCompany = request.form['fileCompany']
        dashboard.fileDepartment = request.form['fileDepartment']

        selected_users = request.form.getlist('usuarios')

        # Atualizar os usuários associados ao dashboard
        current_users = db.session.query(files_users).filter_by(idfiles=id).all()
        current_user_ids = [user.idusers for user in current_users]

        for user_id in selected_users:
            if int(user_id) not in current_user_ids:
                new_access = files_users.insert().values(idfiles=id, idusers=int(user_id))
                db.session.execute(new_access)

        for user in current_users:
            if str(user.idusers) not in selected_users:
                delete_access = files_users.delete().where(
                    files_users.c.idfiles == id,
                    files_users.c.idusers == user.idusers
                )
                db.session.execute(delete_access)

        db.session.commit()
        return redirect(url_for('config'))

    usuarios = users.query.all()
    usuarios_selecionados = [user.idusers for user in db.session.query(files_users).filter_by(idfiles=id).all()]

    return render_template('editar_dashboard.html', dashboard=dashboard, usuarios=usuarios,
                           usuarios_selecionados=usuarios_selecionados)


@app.route('/excluir_dashboard/<int:dashboard_id>', methods=['POST'])
def excluir_dashboard(dashboard_id):
    dashboard = files.query.get_or_404(dashboard_id)

    # Excluir associações na tabela files_users
    db.session.query(files_users).filter(files_users.c.idfiles == dashboard_id).delete()

    # Agora pode excluir o dashboard
    db.session.delete(dashboard)
    db.session.commit()
    return redirect(url_for('config'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

