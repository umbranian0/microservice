from flask import Blueprint, request, jsonify, make_response
from models import Artigo, db

artigo_blueprint = Blueprint('artigo_api_routes', __name__, url_prefix='/api/artigo')

@artigo_blueprint.route('/todos', methods=['GET'])
def get_todos_artigos():
    todos_artigos = Artigo.query.all()
    result = [artigo.serializar() for artigo in todos_artigos]
    response = {
        'message': 'Todos os Artigos',
        'result': result
    }
    return jsonify(response)

@artigo_blueprint.route('/criar', methods=['POST'])
def criar_artigo():
    try:
        descricao = request.form.get('descricao')
        codigoArtigo = request.form.get('codigoArtigo')
        preco = request.form.get('preco')
        imagem = request.form.get('imagem')
        
        if not descricao or not codigoArtigo:
            response = {
                'message': 'Descricao e CodigoArtigo sao obrigatorios.'
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
    return jsonify(response)

@artigo_blueprint.route('/<cA>', methods=['GET'])
def detalhes_Artigo(cA):
    artigo = Artigo.query.filter_by(codigoArtigo=cA).first()
    if artigo:
        response = {'result': artigo.serializar()}
    else:
        response = {'message': 'Sem artigos criados.'}
    return jsonify(response)
