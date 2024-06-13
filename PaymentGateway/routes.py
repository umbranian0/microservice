from flask_restx import Namespace, Resource, fields

# Initialize namespace
payment_ns = Namespace('payment', description='Payment operations')

# Define the payment model
payment_model = payment_ns.model('Payment', {
    'Id': fields.Integer(required=True, description='The payment identifier'),
    'CustomerId': fields.String(required=True, description='The customer identifier'),
    'PaymentTypeId': fields.Integer(required=True, description='The type of payment'),
    'TotalAmount': fields.Float(required=True, description='The total amount of the payment'),
    'Fee': fields.Float(required=True, description='The fee for the payment'),
    'IsPaid': fields.Boolean(required=True, description='The payment status')
})

# Sample data (you may replace it with database operations)
payments = []

@payment_ns.route('/AcknowledgePayment')
class AcknowledgePayment(Resource):
    @payment_ns.param('PaymentID', 'The payment identifier')
    def get(self):
        payment_id = payment_ns.payload['PaymentID']
        payment = next((payment for payment in payments if payment['Id'] == payment_id), None)
        if payment:
            return {'message': 'Payment acknowledged.', 'payment': payment}, 200
        return {'message': 'Payment not found.'}, 404

@payment_ns.route('/CreatePayment')
class CreatePayment(Resource):
    @payment_ns.expect(payment_model)
    def post(self):
        payment = payment_ns.payload
        payments.append(payment)
        return {'message': 'Payment created.', 'payment': payment}, 201
