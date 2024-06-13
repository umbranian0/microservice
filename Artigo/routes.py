from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from health import HealthCheck
from models import Artigo, db

api = Namespace('artigo', description='Artigo related operations')

# Define the authorization header
authorization = api.parser()
authorization.add_argument('Authorization', location='headers', required=True, help='Bearer Token')

# Model for creating an article
artigo_fields = api.model('Artigo', {
    'descricao': fields.String(required=True, description='Descrição do artigo'),
    'codigoArtigo': fields.String(required=True, description='Código do artigo'),
    'preco': fields.Float(required=False, description='Preço do artigo'),
    'imagem': fields.String(required=False, description='Imagem do artigo')
})
@api.route('/_health')
class HealthCheckResource(Resource):
    def get(self):
        database_status = HealthCheck.check_database_status()
        if database_status == 'OK':
            return {'status': 'OK', 'database': 'OK'}, 200
        else:
            return {'status': 'Error', 'database': 'Error'}, 500
        
        
@api.route('/todos')
class GetTodosArtigos(Resource):
    def get(self):
        todos_artigos = Artigo.query.all()
        result = [artigo.serializar() for artigo in todos_artigos]
        response = {
            'message': 'Todos os Artigos',
            'result': result
        }
        return jsonify(response)

@api.route('/criar')
class CriarArtigo(Resource):
    @api.expect(authorization, artigo_fields)
    def post(self):
        try:
            args = authorization.parse_args()
            api_key = args['Authorization']
            if not api_key:
                return {'message': 'Authorization header missing'}, 400

            data = request.json
            descricao = data.get('descricao')
            codigoArtigo = data.get('codigoArtigo')
            preco = data.get('preco')
            imagem = data.get('imagem')

            if not descricao or not codigoArtigo:
                response = {
                    'message': 'Descricao e CodigoArtigo são obrigatórios.'
                }
                return jsonify(response), 400

            artigo = Artigo(
                descricao=descricao,
                codigoArtigo=codigoArtigo,
                preco=preco,
                imagem=imagem
            )
            db.session.add(artigo)
            db.session.commit()
            response = {
                'message': 'Artigo criado com sucesso.',
                'result': artigo.serializar()
            }
        except Exception as e:
            print(str(e))
            response = {'message': 'Erro na criação do artigo.'}
            return jsonify(response), 500
        return jsonify(response)

@api.route('/<cA>')
class DetalhesArtigo(Resource):
    def get(self, cA):
        artigo = Artigo.query.filter_by(codigoArtigo=cA).first()
        if artigo:
            response = {'result': artigo.serializar()}
        else:
            response = {'message': 'Sem artigos criados.'}
        return jsonify(response)
