import datetime
from urllib import request
from flask import Blueprint, jsonify, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restx import Namespace, Resource, fields
from models import Utilizador, db
from flask_login import login_user, current_user, logout_user
from health import HealthCheck

##var
utilizador_blueprint = Blueprint('utilizador_api_routes', __name__, url_prefix='/api/utilizador')
api = Namespace('Utilizador',doc='/swagger/', description='Utilizador operations')

# Define models for request and response payloads
utilizador_model = api.model('Utilizador', {
    'nomeUtilizador': fields.String(required=True, description='Nome do utilizador'),
    'password': fields.String(required=True, description='Senha do utilizador')
})
#healthcheck
@api.route('/_health')
class HealthCheckResource(Resource):
    def get(self):
        database_status = HealthCheck.check_database_status()
        if database_status == 'OK':
            return {'status': 'OK', 'database': 'OK'}, 200
        else:
            return {'status': 'Error', 'database': 'Error'}, 500
        
#get all
@api.route('/')
class UtilizadorList(Resource):
    @api.doc(responses={200: 'Success', 500: 'Internal Server Error'})
    def get(self):
        """List all utilizadores"""
        todos_utilizadores = Utilizador.query.all()
        result = [utilizador.serializar() for utilizador in todos_utilizadores]
        return jsonify({'message': 'Todos os Utilizadores', 'result': result})

    @api.doc(responses={201: 'Created', 400: 'Bad Request', 500: 'Internal Server Error'})
    @api.expect(utilizador_model)
    def post(self):
        """Create a new utilizador"""
        data = request.json
        nomeUtilizador = data.get('nomeUtilizador')
        password = data.get('password')

        if not nomeUtilizador or not password:
            return {'message': 'Nome de utilizador e senha são obrigatórios.'}, 400

        utilizador = Utilizador(nomeUtilizador=nomeUtilizador, password=generate_password_hash(password))
        db.session.add(utilizador)
        db.session.commit()

        return {'message': 'Utilizador criado com sucesso.', 'result': utilizador.serializar()}, 201


@api.route('/<string:nomeUtilizador>/login')
class UtilizadorLogin(Resource):
    @api.doc(responses={200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @api.expect(utilizador_model)
    def post(self, nomeUtilizador):
        """Login a utilizador"""
        data = request.json
        password = data.get('password')

        utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()

        if not utilizador or not check_password_hash(utilizador.password, password):
            return {'message': 'Autenticação incorreta'}, 401

        login_user(utilizador)
        return {'message': 'Conectado','result':utilizador.serializar()}, 200


@api.route('/logout')
class UtilizadorLogout(Resource):
    @api.doc(responses={200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'})
    def post(self):
        """Logout current utilizador"""
        if current_user.is_authenticated:
            logout_user()
            return {'message': 'Desconectado'}, 200
        return {'message': 'Não existem utilizadores conectados'}, 401


@api.route('/<string:nomeUtilizador>/existe')
class UtilizadorExist(Resource):
    @api.doc(responses={200: 'Success', 404: 'Not Found', 500: 'Internal Server Error'})
    def get(self, nomeUtilizador):
        """Check if utilizador exists"""
        utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()
        if utilizador:
            return {'message': True}, 200
        return {'message': False}, 404


@api.route('/current')
class CurrentUtilizador(Resource):
    @api.doc(responses={200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'})
    def get(self):
        """Get current utilizador"""
        if current_user.is_authenticated:
            return {'result': current_user.serializar()}, 200
        else:
            return {'message': 'Utilizador não conectado'}, 401


@api.route('/<string:nomeUtilizador>/update-api-key')
class UpdateAPIKey(Resource):
    @api.doc(responses={200: 'Success', 401: 'Unauthorized', 404: 'Not Found', 500: 'Internal Server Error'})
    def post(self, nomeUtilizador):
        """Update API Key for utilizador"""
        utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()
        if utilizador:
            utilizador.update_api_key()
            db.session.commit()
            login_user(utilizador)
            return {'message': 'Conectado', 'api_key': utilizador.api_key}, 200
        return {'message': 'Utilizador não encontrado'}, 404

