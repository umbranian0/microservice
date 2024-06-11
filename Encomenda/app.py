from flask import Flask
from flask_migrate import Migrate
import models
import os
from routes import encomenda_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'j5sFMBkzzUV4DUTEQzxqFw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

file_path = os.path.abspath(os.path.join(os.getcwd(), 'database', 'encomenda.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path

models.init_app(app)

app.register_blueprint(encomenda_blueprint)

migrate = Migrate(app, models.db)
#db.create_all()
@app.route('/')
def index():
    return "hello world"

if __name__ == '__main__':
    app.run(debug=True, port=5003)
