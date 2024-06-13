import requests
from __init__ import ENCOMENDA_API_URL

class EncomendaApi:
    @staticmethod
    def get_encomenda():
        header = {'Authorization':session['utilizador_api_key']}

        response = requests.get(ENCOMENDA_API_URL+'api/encomenda',headers=header)
        return response.json()

    @staticmethod
    def adicionar_ao_carrinho(artigoId,quantidade=1):
        payload={
            'artigoId':artigoId,
            'quantidade': quantidade
        }
        header = {'Authorization':session['utilizador_api_key']}

        response = requests.post(ENCOMENDA_API_URL+'/api/encomenda/adicionarArtigo',data=payload,headers=header)

        return response.json()
    

    @staticmethod
    def checkout():
        header = {'Authorization':session['utilizador_api_key']}
        response = requests.post(ENCOMENDA_API_URL+'/api/encomenda/checkout',headers=header)
        return response.json()
    
    @staticmethod
    def get_encomenda_da_sessao():
        encomenda_default = {
            'items':{}
        }
        return session.get('encomenda',encomenda_default)
    
    