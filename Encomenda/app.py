import logging
import os
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db
import models 
from routes import encomenda_blueprint
from routes import api as encomenda_api_routes

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'j5sFMBkzzUV4DUTEQzxqFw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'encomenda.db'))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

models.init_app(app)

app.register_blueprint(encomenda_blueprint)

migrate = Migrate(app, db)

# Initialize Flask-RESTx
api = Api(app, title='Encomenda API',doc='/swagger/', description='A microservice for encomenda processing')
api.add_namespace(encomenda_api_routes, path='/api/encomenda')

if __name__ == '__main__':
    logging.debug("Starting the application.")
    app.run(debug=True, port=5003)
