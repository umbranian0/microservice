# Inside routes.py

from flask import request
from flask_restx import Namespace, Resource, fields
from models import Payment, acknowledge_payment_in_gateway
from health import HealthCheck

#initialize payment namespace and services        
payment_ns = Namespace('paymentGateway', description='Payment operations')

payment_model = payment_ns.model('Payment', {
    'CustomerId': fields.String(required=True, description='The customer identifier'),
    'PaymentTypeId': fields.Integer(required=True, description='The type of payment'),
    'TotalAmount': fields.Float(required=True, description='The total amount of the payment'),
    'Fee': fields.Float(required=False, description='The fee for the payment'),
    'IsPaid': fields.Boolean(description='The payment status', default=False)
})

@payment_ns.route('/_health')
class HealthCheckResource(Resource):
    def get(self):
        database_status = HealthCheck.check_database_status()
        if database_status == 'OK':
            return {'status': 'OK', 'database': 'OK'}, 200
        else:
            return {'status': 'Error', 'database': 'Error'}, 500

@payment_ns.route('/CreatePayment')
class CreatePayment(Resource):
    @payment_ns.expect(payment_model)
    def post(self):
        new_payment_data = payment_ns.payload
        try:
            payment = Payment.create_payment(new_payment_data)
            return {'message': 'Payment created successfully.', 'payment': payment.to_dict()}, 201
        except Exception as e:
            return {'message': f'Error creating payment: {e}'}, 500

@payment_ns.route('/AcknowledgePayment')
class AcknowledgePayment(Resource):
    @payment_ns.doc(params={'PaymentID': 'The payment identifier'})
    def get(self):
        payment_id = request.args.get('PaymentID')
        if not payment_id:
            return {'message': 'PaymentID parameter is required.'}, 400

        payment = Payment.query.get(payment_id)
        if not payment:
            return {'message': 'Payment not found.'}, 404

        if payment.is_paid:
            return {'message': 'Payment is already acknowledged.'}, 400

        try:
            response = acknowledge_payment_in_gateway(payment_id)
            payment.update_payment_status(payment_id, is_paid=True)
            return {'message': 'Payment acknowledged.', 'payment': payment.to_dict()}, 200
        except Exception as e:
            return {'message': f'Error acknowledging payment: {e}'}, 500

@payment_ns.route('/PendingPayments')
class PendingPayments(Resource):
    @payment_ns.doc(params={
        'customerId': 'Filter by customer ID',
        'paymentTypeId': 'Filter by payment type ID',
        'minAmount': 'Filter by minimum amount',
        'maxAmount': 'Filter by maximum amount'
    })
    def get(self):
        filters = {
            'customer_id': request.args.get('customerId'),
            'payment_type_id': request.args.get('paymentTypeId'),
            'min_amount': request.args.get('minAmount'),
            'max_amount': request.args.get('maxAmount')
        }

        # Remove None values from filters
        filters = {k: v for k, v in filters.items() if v is not None}

        try:
            pending_payments = Payment.get_pending_payments(filters)
            return {'pending_payments': [payment.to_dict() for payment in pending_payments]}, 200
        except ValueError as e:
            return {'message': f'Invalid filter value: {e}'}, 400
