from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)

class Encomenda(db.Model):
    __tablename__ = 'encomenda'
    id = db.Column(db.Integer, primary_key=True)
    utilizadorId = db.Column(db.Integer)
    aberta = db.Column(db.Boolean, default=False)
    linhas_encomenda = db.relationship('EncomendaLinha',backref="linhaEncomenda")

    def __repr__(self):
        return f'<encomenda {self.id}>'

    def serializar(self):
        return {
            'id': self.id,
            'utilizadorId': self.utilizadorId,
            'aberta': self.aberta,
            'linhas_encomenda': [x.serializar() for x in self.linhas_encomenda],
           
        }

class EncomendaLinha(db.Model):
    __tablename__ = 'linhaEncomenda'
    id = db.Column(db.Integer, primary_key=True)
    encomendaId = db.Column(db.Integer, db.ForeignKey('encomenda.id'))
    artigoId = db.Column(db.Integer)
    quantidade = db.Column(db.Float)
    def __repr__(self):
        return f'<encomenda {self.id}>'
    def serializar(self):
        return {
            'id': self.id,
            'artigo': self.artigoId,
            'quantidade': self.quantidade,
           
        }