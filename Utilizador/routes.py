from flask import Blueprint, request, jsonify, make_response
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Utilizador, db

utilizador_blueprint = Blueprint('utilizador_api_routes', __name__, url_prefix='/api/utilizador')

@utilizador_blueprint.route('/todos', methods=['GET'])
def get_todos_utilizadores():
    todos_utilizadores = Utilizador.query.all()
    result = [utilizador.serializar() for utilizador in todos_utilizadores]
    response = {
        'message': 'Todos os Utilizadores',
        'result': result
    }
    return jsonify(response)

@utilizador_blueprint.route('/criar', methods=['POST'])
def criar_utilizador():
    try:
        nomeUtilizador = request.form.get('nomeUtilizador')
        password = request.form.get('password')
        if not nomeUtilizador or not password:
            response = {
                'message': 'Nome de utilizador e senha sao obrigatorios.'
            }
            return jsonify(response), 400
        
        utilizador = Utilizador()
        utilizador.nomeUtilizador = nomeUtilizador
        utilizador.password = generate_password_hash(password, method='pbkdf2:sha256')
        utilizador.administrador = False
        db.session.add(utilizador)
        db.session.commit()
        response = {
            'message': 'Utilizador criado com sucesso.',
            'result': utilizador.serializar()
        }
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro na criação do utilizador.'}
    return jsonify(response)

@utilizador_blueprint.route('/login', methods=['POST'])
def login():
    nomeUtilizador = request.form['nomeUtilizador']
    password = request.form['password']

    utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()

    if not utilizador:
        response = {'message': 'Este utilizador nao existe'}
        return make_response(jsonify(response), 401)
    if check_password_hash(utilizador.password, password):
        utilizador.update_api_key()
        db.session.commit()
        login_user(utilizador)
        response = {'message': 'Connecting', 'api_key': utilizador.api_key}
        return make_response(jsonify(response), 200)
    response = {'message': 'Autenticacao incorreta'}
    return make_response(jsonify(response), 401)

@utilizador_blueprint.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Desconectado'})
    return jsonify({'message': 'Não existem utilizadores conectados'})

@utilizador_blueprint.route('/<nomeUtilizador>/existe', methods=['GET'])
def get_utilizador_existe(nomeUtilizador):
    utilizador = Utilizador.query.filter_by(nomeUtilizador=nomeUtilizador).first()
    if utilizador:
        return jsonify({'message': True}), 200
    return jsonify({'message': False}), 404

@utilizador_blueprint.route('/', methods=['GET'])
def get_utilizador_atual():
    if current_user.is_authenticated:
        return jsonify({'result': current_user.serializar()}), 200
    else:
        return jsonify({'message': 'user nao conectado'}), 401
