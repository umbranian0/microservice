import requests
from __init__ import UTILIZADOR_API_URL

class UtilizadorApi:
    @staticmethod
    def login(form):
        api_key=None
        payload={
            'nomeUtilizador': form.nomeUtilizador.data,
            'password': form.password.data
        }

        url = UTILIZADOR_API_URL +'/api/utilizador/login'

        response = requests.post(url,data=payload)
        if response:
            api_key = response.json().get('api_key')
        return api_key
    
    @staticmethod
    def get_utilizador():
        headers = {
            'Authorization':session['utilizador_api_key']
        }

        url = UTILIZADOR_API_URL + '/api/utilizador'
        response = requests.get(url,headers=headers)
        return response.json()
    
    @staticmethod
    def criar_utilizador(form):
        utilizador = None 
        payload={
            'nomeUtilizador': form.nomeUtilizador.data,
            'password': form.password.data
        }
        url = UTILIZADOR_API_URL +'/api/utilizador/'

        response = requests.post(url,data=payload)
        if response:
            utilizador=response.json()
        return utilizador
    
    @staticmethod
    def get_utilizador_existente(nomeUtilizador):
        url = UTILIZADOR_API_URL + '/api/utilizador/'+nomeUtilizador+'/existe'

        response = requests.get(url)
        return response.json()
