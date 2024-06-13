from flask import Flask
from flask_restx import Api
from routes import payment_ns
from models import db

# Initialize Flask app and configure
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///payments.db'  # or another database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
api = Api(app, title='Payment API',doc='/swagger/', description='A microservice for payment processing')

# Register namespaces
api.add_namespace(payment_ns, path='/api/paymentGateway')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True, port=5006)
