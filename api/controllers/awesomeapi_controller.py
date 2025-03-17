import requests
from uuid import uuid4
from datetime import datetime
from config import conect_elastic
from config import create_app

def leitura():
    app = create_app()
    es = conect_elastic(app)
    print('leitura: ')
    try:
        
        response = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL,CAD-BRL,EUR-BRL')

        response.raise_for_status()

        data = response.json()

        moedas = [
            {
                'nome': data['USDBRL']['name'],
                'valor': data['USDBRL']['high'],
                'dtLeitura': datetime.strptime(data['USDBRL']['create_date'], "%Y-%m-%d %H:%M:%S")
            },
            {
                'nome': data['CADBRL']['name'],
                'valor': data['CADBRL']['high'],
                'dtLeitura': datetime.strptime(data['CADBRL']['create_date'], "%Y-%m-%d %H:%M:%S")
            },
            {
                'nome': data['EURBRL']['name'],
                'valor': data['EURBRL']['high'],
                'dtLeitura': datetime.strptime(data['EURBRL']['create_date'], "%Y-%m-%d %H:%M:%S")
            },
        ]
        for moeda in moedas:
            es.index(index='moedas', id=str(uuid4()), document=moeda) 
    except Exception as e:
        print(f'Erro ao se comunicar com awesomeAPI: {e}')