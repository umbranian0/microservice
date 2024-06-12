from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)

class Artigo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(250), unique=False)
    codigoArtigo = db.Column(db.String(21), unique=True)
    preco = db.Column(db.Float, nullable=True)
    imagem = db.Column(db.String(255))

    def __repr__(self):
        return f'<artigo {self.id}, {self.descricao}>'

    def serializar(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'codigoArtigo': self.codigoArtigo,
            'preco': self.preco,
            'imagem': self.imagem,
        }
