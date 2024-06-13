from flask_sqlalchemy import SQLAlchemy
import requests

# Define the database object
db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), nullable=False)
    payment_type_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=True, default=0.0)
    is_paid = db.Column(db.Boolean, default=False)

    def __init__(self, id, customer_id, payment_type_id, total_amount, fee, is_paid):
        self.id = id
        self.customer_id = customer_id
        self.payment_type_id = payment_type_id
        self.total_amount = total_amount
        self.fee = fee
        self.is_paid = is_paid

# Function to integrate with the payment gateway for creating a payment
def create_payment_in_gateway(payment_data):
    payment_gateway_url = 'https://vasile-timotin.outsystemscloud.com/PaymentGateway/rest/Payment/CreatePayment'
    try:
        response = requests.post(payment_gateway_url, json=payment_data)
        return response
    except Exception as e:
        print(f"Error creating payment in gateway: {e}")
        raise

# Function to integrate with the payment gateway for acknowledging a payment
def acknowledge_payment_in_gateway(payment_id):
    payment_gateway_url = 'https://vasile-timotin.outsystemscloud.com/PaymentGateway/rest/Payment/AcknolagePayment'
    try:
        response = requests.get(payment_gateway_url, params={'PaymentID': payment_id})
        return response
    except Exception as e:
        print(f"Error acknowledging payment in gateway: {e}")
        raise
