from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import Users, Files, files_users

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.method == 'POST':
        try:
            usuario = Users.query.filter_by(email=request.form['email']).first()
            if usuario and usuario.password == request.form['password']:
                session['usuario_logado'] = usuario.username
                session['departament'] = usuario.departament
                session['username'] = usuario.username
                session['company'] = usuario.company
                session['role'] = usuario.role
                session['id'] = usuario.idusers
                return redirect(url_for('dashboard'))
            else:
                flash('Email ou senha incorretos', 'danger')
        except Exception as e:
            flash(f'Ocorreu um erro: {str(e)}', 'danger')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario_logado' in session:
        page = request.args.get('page', 1, type=int)
        per_page = 3

        if session['role'] == 'Administrador':
            arquivos = Files.query.paginate(page=page, per_page=per_page)
        elif session['role'] == 'Gerente de departamento':
            arquivos = Files.query.filter_by(fileDepartment=session['departament'],
                                             fileCompany=session['company']).paginate(page=page, per_page=per_page)
        elif session['role'] == 'Gestor':
            user_id = Users.query.filter_by(username=session['usuario_logado']).first().idusers
            arquivos = db.session.query(Files).join(files_users).filter(files_users.c.idusers == user_id).paginate(
                page=page, per_page=per_page)
        else:
            user_id = Users.query.filter_by(username=session['usuario_logado']).first().idusers
            arquivos = db.session.query(Files).join(files_users).join(Users).filter(
                files_users.c.idusers == user_id).paginate(page=page, per_page=per_page)

        return render_template('dashboard.html', arquivos=arquivos)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

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

    novo_usuario = Users(username=nome, email=email, role=nível, company=empresa, departament=departamento,
                         password=senha)
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('config'))

@app.route('/config')
def config():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    if session['role'] == 'Administrador':
        arquivos = Files.query.all()
    else:
        arquivos = Files.query.filter_by(fileDepartment=session['departament'], fileCompany=session['company']).all()

    # Definindo 'usuarios' como lista vazia como padrão
    usuarios = []

    if session['role'] == 'Administrador':
        usuarios = Users.query.all()
    elif session['role'] == 'Gestor':
        usuarios = Users.query.filter_by(company=session['company']).all()
    elif session['role'] == 'Gerente de departamento':
        usuarios = Users.query.filter_by(company=session['company'], departament=session['departament']).all()

    # Buscar dashboards
    dashboards = Files.query.all()

    return render_template('config.html', dashboards=dashboards, arquivos=arquivos, usuarios=usuarios, titulo='config')

@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if request.method == 'POST':
        senhaAtual = request.form['senhaAtual']
        novaSenha = request.form['novaSenha']
        novaSenhaNovamente = request.form['novaSenhaNovamente']

        user = Users.query.filter_by(idusers=session['id']).first()
        if user.password == senhaAtual:
            if novaSenha == novaSenhaNovamente:
                user.password = novaSenha
                db.session.add(user)
                db.session.commit()

    return render_template('perfil.html')

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

        novo_usuario = Users(username=username, email=email, password=password, company=company,
                             departament=departament, role=role)
        db.session.add(novo_usuario)
        db.session.commit()

        return redirect(url_for('CadastrarUser'))

    return render_template('cadastrar_usuario.html', titulo='CadastrarUser')

@app.route('/CadastrarDashboard', methods=['GET', 'POST'])
def CadastrarDashboard():
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        link = request.form['link']
        company = request.form['company']
        department = request.form['department']
        selected_users = request.form.getlist('usuario')

        novo_arquivo = Files(title=title, link=link, fileDepartment=department, fileCompany=company)
        db.session.add(novo_arquivo)
        db.session.commit()

        file_id = novo_arquivo.idFiles

        for usuario_id in selected_users:
            association = files_users.insert().values(idfiles=file_id, idusers=usuario_id)
            db.session.execute(association)
        db.session.commit()

        return redirect(url_for('CadastrarDashboard'))

    usuarios = []
    if session['role'] == 'Gerente de departamento':
        usuarios = Users.query.filter_by(departament=session['departament'], company=session['company']).all()
    elif session['role'] == 'Gestor':
        usuarios = Users.query.filter_by(company=session['company']).all()
    elif session['role'] == 'Administrador':
        usuarios = Users.query.all()

    return render_template('cadastrar_dashboard.html', titulo='CadastrarDashboard', usuarios=usuarios)

@app.route('/excluir/<int:usuario_id>', methods=['POST'])
def excluirUsuario(usuario_id):
    if 'usuario_logado' not in session:
        return redirect(url_for('index'))

    usuario = Users.query.get(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('config'))

@app.route('/editar_usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Users.query.get(id)

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
    dashboard = Files.query.get_or_404(id)

    if request.method == 'POST':
        dashboard.title = request.form['title']
        dashboard.link = request.form['link']
        dashboard.fileCompany = request.form['company']
        dashboard.fileDepartment = request.form['department']

        selected_users = request.form.getlist('usuarios')
        print(f"Selected users: {selected_users}")  # Depuração

        current_users = db.session.query(files_users).filter_by(idfiles=id).all()
        current_user_ids = [user.idusers for user in current_users]
        print(f"Current users: {current_user_ids}")  # Depuração

        for user_id in selected_users:
            if int(user_id) not in current_user_ids:
                print(f"Adding user {user_id} to file {id}")  # Depuração
                new_access = files_users.insert().values(idfiles=id, idusers=int(user_id))
                db.session.execute(new_access)

        for user in current_users:
            if str(user.idusers) not in selected_users:
                print(f"Removing user {user.idusers} from file {id}")  # Depuração
                delete_access = files_users.delete().where(
                    files_users.c.idfiles == id,
                    files_users.c.idusers == user.idusers
                )
                db.session.execute(delete_access)

        db.session.commit()
        return redirect(url_for('config'))

    usuarios = Users.query.all()
    usuarios_selecionados = [user.idusers for user in db.session.query(files_users).filter_by(idfiles=id).all()]

    return render_template('editar_dashboard.html', dashboard=dashboard, usuarios=usuarios,
                           usuarios_selecionados=usuarios_selecionados)


@app.route('/excluir_dashboard/<int:dashboard_id>', methods=['POST'])
def excluir_dashboard(dashboard_id):
    dashboard = Files.query.get_or_404(dashboard_id)

    db.session.query(files_users).filter(files_users.c.idfiles == dashboard_id).delete()

    db.session.delete(dashboard)
    db.session.commit()
    return redirect(url_for('config'))

if __name__ == '__main__':
    app.run(debug=True)
