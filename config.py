SECRET_KEY = 'root'

"""
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='Gabrielm3l0',
        senha='nikgeo369',
        servidor='Gabrielm3l0.mysql.pythonanywhere-services.com',
        database='Gabrielm3l0$gestao_correta'
    )
"""
SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='root',
        servidor='localhost',
        database='gestao_correta'
    )