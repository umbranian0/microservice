import requests
from __init__ import ARTIGO_API_URL

class ArtigoApi:
    @staticmethod
    def get_artigos():
        response = requests.get(ARTIGO_API_URL+'api/artigo/todos')
        return response.json()
    @staticmethod
    def get_artigo(cA):
        response = requests.get(ARTIGO_API_URL+'api/artigo/'+cA)
        return response.json()
    
