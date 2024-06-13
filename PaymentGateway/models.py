from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy.sql.expression import text
# Define the database object
db = SQLAlchemy()

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), nullable=False)
    payment_type_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=True, default=0.0)
    is_paid = db.Column(db.Boolean, default=False)

    def __init__(self, customer_id, payment_type_id, total_amount, fee=0.0, is_paid=False, id=None):
        if id is not None:
            self.id = id
        self.customer_id = customer_id
        self.payment_type_id = payment_type_id
        self.total_amount = total_amount
        self.fee = fee
        self.is_paid = is_paid

    def to_dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'payment_type_id': self.payment_type_id,
            'total_amount': self.total_amount,
            'fee': self.fee,
            'is_paid': self.is_paid
        }
    
    @classmethod
    def create_payment(cls, payment_data):
        # Send data to the payment gateway
        try:
            response_data = create_payment_in_gateway(payment_data)
            payment_id = response_data  # The response is a string containing the payment ID
            if not payment_id:
                raise Exception('Payment gateway did not return a payment ID.')
        except Exception as e:
            raise Exception(f'Payment creation failed in gateway. Error: {e}')
        
        # Store the payment in the local database with the returned ID
        payment = cls(
            id=payment_id,
            customer_id=payment_data['CustomerId'],
            payment_type_id=payment_data['PaymentTypeId'],
            total_amount=payment_data['TotalAmount'],
            fee=payment_data.get('Fee', 0.0),
            is_paid=False
        )
        db.session.add(payment)
        db.session.commit()
        return payment
    
    @classmethod
    def update_payment_status(cls, payment_id, is_paid):
        payment = cls.query.get(payment_id)
        if payment:
            payment.is_paid = is_paid
            db.session.commit()
            return payment
        return None
    

    @classmethod
    def get_pending_payments(cls, filters=None):
        query = cls.query.filter_by(is_paid=False)  # Only pending payments

        if filters:
            if 'customer_id' in filters:
                query = query.filter_by(customer_id=filters['customer_id'])
            if 'payment_type_id' in filters:
                query = query.filter_by(payment_type_id=filters['payment_type_id'])
            if 'min_amount' in filters and filters['min_amount'] is not None:
                query = query.filter(cls.total_amount >= float(filters['min_amount']))
            if 'max_amount' in filters and filters['max_amount'] is not None:
                query = query.filter(cls.total_amount <= float(filters['max_amount']))

        return query.all()

# Function to integrate with the payment gateway for creating a payment
def create_payment_in_gateway(payment_data):
    payment_gateway_url = 'https://vasile-timotin.outsystemscloud.com/PaymentGateway/rest/Payment/CreatePayment'
    try:
        response = requests.post(payment_gateway_url, json=payment_data)
        response.raise_for_status()
        return response.text  # Return the string content of the response
    except Exception as e:
        print(f"Error creating payment in gateway: {e}")
        raise

# Function to integrate with the payment gateway for acknowledging a payment
def acknowledge_payment_in_gateway(payment_id):
    payment_gateway_url = 'https://vasile-timotin.outsystemscloud.com/PaymentGateway/rest/Payment/AcknolagePayment'
    try:
        response = requests.get(payment_gateway_url, params={'PaymentID': payment_id})
        response.raise_for_status()  # Raise an error for bad status codes
        return response
    except requests.RequestException as e:
        print(f"Error acknowledging payment in gateway: {e}")
        raise
