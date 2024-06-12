from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilizadorId = db.Column(db.Integer, nullable=False)
    aberta = db.Column(db.Boolean, default=True)

    def serializar(self):
        return {
            'id': self.id,
            'utilizadorId': self.utilizadorId,
            'aberta': self.aberta
        }

class EncomendaLinha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    encomendaId = db.Column(db.Integer, db.ForeignKey('encomenda.id'), nullable=False)
    artigoId = db.Column(db.Integer, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    def serializar(self):
        return {
            'id': self.id,
            'encomendaId': self.encomendaId,
            'artigoId': self.artigoId,
            'quantidade': self.quantidade
        }
