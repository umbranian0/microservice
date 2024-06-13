from flask import Flask, g
from flask.sessions import SecureCookieSessionInterface  # Add this import
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_restx import Api
from models import db, init_app
import models
import os
from routes import utilizador_blueprint
from routes import api as utilizador_api_routes


app = Flask(__name__)
app.config['SECRET_KEY'] = 'j5sFMBkzzUV4DUTEQzxqFw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'utilizador.db'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

models.init_app(app)

app.register_blueprint(utilizador_blueprint)
login_manager = LoginManager(app)

migrate = Migrate(app, db)

# Initialize Flask-RESTx
api = Api(app, title='Utilizador API',doc='/swagger/', description='A microservice for user processing')
api.add_namespace(utilizador_api_routes, path='/api/utilizador')

@app.route('/')
def index():
    return "Bem vindo as API do Utilizador"

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        utilizador = models.Utilizador.query.filter_by(api_key=api_key).first()
        if utilizador:
            return utilizador
    return None

class CustomSessionInterface(SecureCookieSessionInterface):
    """ Impedir a criação de sessoes a partir de solicitações de API """
    def save_sessions(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
