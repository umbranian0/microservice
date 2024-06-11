from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)

class Utilizador(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nomeUtilizador = db.Column(db.String(50), unique=False)
    password = db.Column(db.String(250), unique=True)
    administrador = db.Column(db.Boolean)
    api_key = db.Column(db.String(255), unique=True, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    autenticado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'utilizador{self.id}, {self.nomeUtilizador}'

    def serializar(self):
        return {
            'id': self.id,
            'nomeUtilizador': self.nomeUtilizador,
            'administrador': self.administrador,
            'api_key': self.api_key,
            'ativo': self.ativo,
        }

    def update_api_key(self):
        self.api_key = generate_password_hash(self.nomeUtilizador + str(datetime.now(timezone.utc)))
