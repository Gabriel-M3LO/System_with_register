from app import db

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
