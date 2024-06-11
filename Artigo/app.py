from flask import Flask, g
from flask.sessions import SecureCookieSessionInterface
from flask_migrate import Migrate
import models
import os
from routes import artigo_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'j5sFMBkzzUV4DUTEQzxqFw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'artigo.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

models.init_app(app)
app.register_blueprint(artigo_blueprint)

migrate = Migrate(app, models.db)

@app.route('/')
def index():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True, port=5002)
