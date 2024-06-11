import unittest
import json
from unittest.mock import patch
from app import app, db
from models import Encomenda, EncomendaLinha , db

# Create the database tables before running the tests
with app.app_context():
    db.create_all()

class TestEncomendaAPI(unittest.TestCase):
    def setUp(self):
        # Set up test client
        self.app = app.test_client()
        self.app.testing = True

        # Set up test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    @patch('routes.get_utilizador')
    def test_adicionar_artigo(self, mock_get_utilizador):
        mock_get_utilizador.return_value = {'id': 1}  # Mock the response of get_utilizador

        # Simulate user authentication
        headers = {'Authorization': 'your_fake_token'}

        # Send a POST request to add an article
        data = {'artigoId': 1, 'quantidade': 2}
        response = self.app.post('/api/encomenda/adicionarArtigo', headers=headers, json=data)
        data = json.loads(response.data.decode())

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)
        self.assertEqual(data['message'], 'Artigo adicionado à encomenda com sucesso.')

    @patch('routes.get_utilizador')
    def test_checkout(self, mock_get_utilizador):
        mock_get_utilizador.return_value = {'id': 1}  # Mock the response of get_utilizador

        # Simulate user authentication
        headers = {'Authorization': 'your_fake_token'}

        # Send a POST request to checkout
        response = self.app.post('/api/encomenda/checkout', headers=headers)
        data = json.loads(response.data.decode())

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Encomenda finalizada com sucesso.')

    @patch('routes.get_utilizador')
    def test_get_encomenda_pendente(self, mock_get_utilizador):
        mock_get_utilizador.return_value = {'id': 1}  # Mock the response of get_utilizador

        # Simulate user authentication
        headers = {'Authorization': 'your_fake_token'}

        # Send a GET request to get pending orders
        response = self.app.get('/api/encomenda/', headers=headers)
        data = json.loads(response.data.decode())

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)

    def test_get_todos_encomendas(self):
        # Send a GET request to get all orders
        response = self.app.get('/api/encomenda/todos')
        data = json.loads(response.data.decode())

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)

    @patch('routes.get_utilizador')
    def test_criar_encomenda(self, mock_get_utilizador):
        mock_get_utilizador.return_value = {'id': 1}  # Mock the response of get_utilizador

        # Simulate user authentication
        headers = {'Authorization': 'your_fake_token'}

        # Send a POST request to create an order
        response = self.app.post('/api/encomenda/criar', headers=headers)
        data = json.loads(response.data.decode())

        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn('result', data)
        self.assertEqual(data['message'], 'Encomenda criada com sucesso.')

    def test_detalhes_encomenda(self):
        # Send a GET request to get details of a specific order
        response = self.app
