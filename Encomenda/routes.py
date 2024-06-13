# routes.py
from flask import Blueprint, request, jsonify
import requests
from flask_restx import Api, Resource, fields
from models import Encomenda, EncomendaLinha, db

# Define the blueprint for encomenda routes
encomenda_blueprint = Blueprint('encomenda_api_routes', __name__, url_prefix='/api/encomenda')
api = Api(encomenda_blueprint, doc='/swagger/')

# Define authorization header
authorization = api.parser()
authorization.add_argument('Authorization', location='headers', required=True, help='Bearer Token')


# URL for the Utilizador API
UTILIZADOR_API_URL = 'http://127.0.0.1:5001/api/utilizador'

# Function to get user information from the Utilizador microservice
def get_utilizador(api_key):
    headers = {'Authorization': api_key}
    response = requests.get(UTILIZADOR_API_URL, headers=headers)
    if response.status_code != 200:
        return {'message': 'Não autorizado.'}
    return response.json()

# Model for adding an article to the order
encomenda_fields = api.model('Encomenda', {
    'artigoId': fields.Integer(required=True, description='ID do artigo'),
    'quantidade': fields.Integer(required=True, description='Quantidade do artigo')
})

# Model for creating an order
criar_encomenda_fields = api.model('CriarEncomenda', {
    'utilizadorId': fields.Integer(required=True, description='ID do utilizador')
})

@api.route('/adicionarArtigo')
class AdicionarArtigo(Resource):
    @api.expect(authorization, encomenda_fields)
    def post(self):
        try:
            args = authorization.parse_args()
            api_key = args['Authorization']
            if not api_key:
                return {'message': 'Authorization header missing'}, 400

            utilizador = get_utilizador(api_key)
            if 'message' in utilizador:
                return utilizador, 401

            data = request.json
            if not all(key in data for key in ['artigoId', 'quantidade']):
                return {'message': 'Missing required parameters'}, 400

            utilizador_id = utilizador.get('id')
            if not utilizador_id:
                return {'message': 'User ID missing in response from Utilizador service'}, 400

            encomenda = Encomenda.query.filter_by(utilizadorId=utilizador_id, aberta=True).first()
            if not encomenda:
                encomenda = Encomenda(utilizadorId=utilizador_id, aberta=True)
                db.session.add(encomenda)
                db.session.commit()

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
            logging.error(f"Error adding article to order: {e}")
            response = {'message': 'Erro ao adicionar artigo à encomenda.'}
            return response, 500
        return response, 200

@api.route('/criar')
class CriarEncomenda(Resource):
    @api.expect(authorization, criar_encomenda_fields)
    def post(self):
        try:
            args = authorization.parse_args()
            api_key = args['Authorization']
            if not api_key:
                return {'message': 'Authorization header missing'}, 400

            utilizador = get_utilizador(api_key)
            if 'message' in utilizador:
                return utilizador, 401

            utilizador_id = utilizador.get('id')
            if not utilizador_id:
                return {'message': 'User ID missing in response from Utilizador service'}, 400

            encomenda = Encomenda(utilizadorId=utilizador_id, aberta=True)
            db.session.add(encomenda)
            db.session.commit()

            response = {
                'message': 'Encomenda criada com sucesso.',
                'result': encomenda.serializar()
            }
        except Exception as e:
            logging.error(f"Error creating order: {e}")
            response = {'message': 'Erro na criação da encomenda.'}
            return response, 500
        return response, 200

@api.route('/todos')
class GetTodosEncomendas(Resource):
    def get(self):
        try:
            todas_encomendas = Encomenda.query.all()
            response = [encomenda.serializar() for encomenda in todas_encomendas]
            return jsonify(response)
        except Exception as e:
            logging.error(f"Error retrieving all orders: {e}")
            return {'message': 'Erro ao obter todas as encomendas.'}, 500

@api.route('/pendente')
class GetEncomendaPendente(Resource):
    @api.expect(authorization)
    def get(self):
        try:
            args = authorization.parse_args()
            api_key = args['Authorization']
            if not api_key:
                return {'message': 'Authorization header missing'}, 400

            utilizador = get_utilizador(api_key)
            if 'message' in utilizador:
                return utilizador, 401

            utilizador_id = utilizador.get('id')
            if not utilizador_id:
                return {'message': 'User ID missing in response from Utilizador service'}, 400

            encomenda = Encomenda.query.filter_by(utilizadorId=utilizador_id, aberta=True).first()
            if encomenda:
                return encomenda.serializar()
            else:
                return {'message': 'No pending orders found for the user.'}, 404
        except Exception as e:
            logging.error(f"Error retrieving pending order: {e}")
            return {'message': 'Erro ao obter a encomenda pendente.'}, 500


@api.route('/checkout')
class Checkout(Resource):
    @api.expect(authorization)
    def post(self):
        try:
            args = authorization.parse_args()
            api_key = args['Authorization']
            if not api_key:
                return {'message': 'Authorization header missing'}, 400

            utilizador = get_utilizador(api_key)
            if 'message' in utilizador:
                return utilizador, 401

            utilizador_id = utilizador.get('id')
            if not utilizador_id:
                return {'message': 'User ID missing in response from Utilizador service'}, 400

            encomenda = Encomenda.query.filter_by(utilizadorId=utilizador_id, aberta=True).first()
            if not encomenda:
                return {'message': 'No open orders found for the user.'}, 404

            # Prepare payment data
            payment_data = {
                "Id": encomenda.id,  # Payment ID should be unique
                "CustomerId": utilizador_id,
                "PaymentTypeId": 1,  # Assuming a fixed payment type for now
                "TotalAmount": encomenda.total_amount,  # Assuming `total_amount` is a property of Encomenda
                "Fee": encomenda.fee,  # Assuming `fee` is a property of Encomenda
                "IsPaid": False
            }

            # Send request to Payment service
            payment_service_url = 'http://payment-service-url/payment/create'  # Replace with actual URL
            response = requests.post(payment_service_url, json=payment_data)

            if response.status_code == 200:
                encomenda.aberta = False
                db.session.commit()
                return {'message': 'Checkout completed successfully and payment processed.'}, 200
            else:
                return {'message': 'Error processing payment', 'details': response.text}, 400

        except Exception as e:
            logging.error(f"Error during checkout: {e}")
            return {'message': 'Erro no checkout.'}, 500