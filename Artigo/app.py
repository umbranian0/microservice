from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api
import models
import os
from routes import api as artigo_api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'j5sFMBkzzUV4DUTEQzxqFw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'artigo.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

models.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, models.db)

if __name__ == '__main__':
    app.run(debug=True, port=5002)
