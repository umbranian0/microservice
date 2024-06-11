from flask import Blueprint, request, jsonify
from models import Encomenda, EncomendaLinha, db
import requests

encomenda_blueprint = Blueprint('encomenda_api_routes', __name__, url_prefix='/api/encomenda')

@encomenda_blueprint.route('/todos', methods=['GET'])
def get_todos_encomendas():
    todos_encomendas = Encomenda.query.all()
    result = [encomenda.serializar() for encomenda in todos_encomendas]
    response = {
        'message': 'Todos os encomendas',
        'result': result
    }
    return jsonify(response)

@encomenda_blueprint.route('/criar', methods=['POST'])
def criar_encomenda():
    try:
        utilizadorId = request.form.get('utilizadorId')
        aberta = request.form.get('aberta', type=bool)

        # Verify the user exists in the Utilizador microservice
        user_response = requests.get(f'http://localhost:5001/api/utilizador/{utilizadorId}/existe')
        if user_response.status_code != 200 or not user_response.json().get('message'):
            response = {'message': 'Utilizador não encontrado.'}
            return jsonify(response), 400

        if utilizadorId is None:
            response = {
                'message': 'utilizadorId é obrigatório.'
            }
            return jsonify(response), 400
        
        encomenda = Encomenda(
            utilizadorId=utilizadorId,
            aberta=aberta
        )
        db.session.add(encomenda)
        db.session.commit()
        response = {
            'message': 'Encomenda criada com sucesso.',
            'result': encomenda.serializar()
        }
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro na criação da encomenda.'}
    return jsonify(response)

@encomenda_blueprint.route('/<int:cA>', methods=['GET'])
def detalhes_encomenda(cA):
    encomenda = Encomenda.query.filter_by(id=cA).first()
    if encomenda:
        response = {'result': encomenda.serializar()}
    else:
        response = {'message': 'Sem encomendas criadas.'}
    return jsonify(response)

@encomenda_blueprint.route('/adicionar_linha', methods=['POST'])
def adicionar_linha_encomenda():
    try:
        encomendaId = request.form.get('encomendaId')
        artigoId = request.form.get('artigoId')
        quantidade = request.form.get('quantidade', type=float)
        
        if not encomendaId or not artigoId or quantidade is None:
            response = {
                'message': 'encomendaId, artigoId e quantidade são obrigatórios.'
            }
            return jsonify(response), 400
        
        linha_encomenda = EncomendaLinha(
            encomendaId=encomendaId,
            artigoId=artigoId,
            quantidade=quantidade
        )
        db.session.add(linha_encomenda)
        db.session.commit()
        response = {
            'message': 'Linha de encomenda adicionada com sucesso.',
            'result': linha_encomenda.serializar()
        }
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro ao adicionar linha de encomenda.'}
    return jsonify(response)
