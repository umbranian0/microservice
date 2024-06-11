from flask import Blueprint, jsonify, request
import requests
from models import Encomenda, EncomendaLinha, db

# Define the blueprint for encomenda routes
encomenda_blueprint = Blueprint('encomenda_api_routes', __name__, url_prefix='/api/encomenda')

# URL for the Utilizador API
UTILIZADOR_API_URL = 'http://127.0.0.1:5001/api/utilizador'

# Function to get user information from the Utilizador microservice
def get_utilizador(api_key):
    headers = {
        'Authorization': api_key
    }
    response = requests.get(UTILIZADOR_API_URL, headers=headers)
    if response.status_code != 200:
        return {'message': 'Não autorizado.'}
    return response.json()

# Route to add an article to the order
@encomenda_blueprint.route('/adicionarArtigo', methods=['POST'])
def adicionar_artigo():
    try:
        # Get the API key from the request headers
        api_key = request.headers.get('Authorization')
        if not api_key:
            return jsonify({'message': 'Authorization header missing'}), 400

        # Get user information using the API key
        utilizador = get_utilizador(api_key)
        if 'message' in utilizador:
            return jsonify(utilizador), 401

        # Extract article data from the request
        data = request.json
        if not all(key in data for key in ['artigoId', 'quantidade']):
            return jsonify({'message': 'Missing required parameters'}), 400

        # Get user ID
        utilizador_id = utilizador.get('id')
        if not utilizador_id:
            return jsonify({'message': 'User ID missing in response from Utilizador service'}), 400

        # Check if there is an open order for the user, if not, create one
        encomenda = Encomenda.query.filter_by(utilizadorId=utilizador_id, aberta=True).first()
        if not encomenda:
            encomenda = Encomenda(utilizadorId=utilizador_id, aberta=True)
            db.session.add(encomenda)
            db.session.commit()

        # Add the article to the order
        linha_encomenda = EncomendaLinha(
            encomendaId=encomenda.id,
            artigoId=data['artigoId'],
            quantidade=data['quantidade']
        )
        db.session.add(linha_encomenda)
        db.session.commit()

        response = {
            'message': 'Artigo adicionado à encomenda com sucesso.',
            'result': linha_encomenda.serializar()
        }
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro ao adicionar artigo à encomenda.'}
    return jsonify(response)

# Route for checkout
@encomenda_blueprint.route('/checkout', methods=['POST'])
def checkout():
    try:
        # Get the API key from the request headers
        api_key = request.headers.get('Authorization')
        if not api_key:
            return jsonify({'message': 'Authorization header missing'}), 400

        # Get user information using the API key
        utilizador = get_utilizador(api_key)
        if 'message' in utilizador:
            return jsonify(utilizador), 401

        # Get user ID
        utilizador_id = utilizador.get('id')
        if not utilizador_id:
            return jsonify({'message': 'User ID missing in response from Utilizador service'}), 400

        # Check if the user has a pending order
        encomenda_pendente = Encomenda.query.filter_by(utilizadorId=utilizador_id, aberta=True).first()
        if not encomenda_pendente:
            return jsonify({'message': 'Sem encomenda pendente para finalizar.'}), 400

        # Close the order
        encomenda_pendente.aberta = False
        db.session.commit()

        response = {'message': 'Encomenda finalizada com sucesso.'}
    except Exception as e:
        print(str(e))
        response = {'message': 'Erro ao finalizar encomenda.'}
    return jsonify(response)


@encomenda_blueprint.route('/', methods=['GET'])
def get_encomenda_pendente():
    api_key = request.header.get('Authorization')
    if not api_key:
        return jsonify({'message':'Nao esta autorizado'}),401
    response =get_utilizador(api_key)
    utilizador = response.get('result')
    if not utilizador:
        return jsonify({'message':'Nao esta autrizado'}),401
    
    encomendaPendende = Encomenda.query.filter_by(utilizadorId = utilizador['id'], aberta=1).first()
    if encomendaPendende:
        return jsonify({'result':encomendaPendende.serializar()}),200
    else:
        return jsonify({'message':'Sem encomendas pendentes.'}),200


# Route to get all encomendas
@encomenda_blueprint.route('/todos', methods=['GET'])
def get_todos_encomendas():
    todas_encomendas = Encomenda.query.all()
    result = [encomenda.serializar() for encomenda in todas_encomendas]
    response = {
        'message': 'Todas as encomendas',
        'result': result
    }
    return jsonify(response)

# Route to create a new encomenda
@encomenda_blueprint.route('/criar', methods=['POST'])
def criar_encomenda():
    try:
        # Get the API key from the request headers
        api_key = request.headers.get('Authorization')
        if not api_key:
            return jsonify({'message': 'Authorization header missing'}), 400

        # Get user information using the API key
        utilizador = get_utilizador(api_key)
        if 'message' in utilizador:
            return jsonify(utilizador), 401

        utilizador_id = utilizador.get('id')
        if not utilizador_id:
            return jsonify({'message': 'User ID missing in response from Utilizador service'}), 400

        # Create a new encomenda
        encomenda = Encomenda(utilizadorId=utilizador_id, aberta=True)
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

# Route to get details of a specific encomenda by id
@encomenda_blueprint.route('/<int:encomenda_id>', methods=['GET'])
def detalhes_encomenda(encomenda_id):
    encomenda = Encomenda.query.get(encomenda_id)
    # Get the API key from the request headers
    api_key = request.headers.get('Authorization')
    if not api_key:
        return jsonify({'message': 'Authorization header missing'}), 400
    
    if encomenda:
        response = {'result': encomenda.serializar()}
    else:
        response = {'message': 'Sem encomendas criadas.'}
    return jsonify(response)
