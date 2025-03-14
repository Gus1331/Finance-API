import requests
from uuid import uuid4

def leitura(es):
    print('leitura: ')
    try:
        
        response = requests.get('https://economia.awesomeapi.com.br/json/last/USD-BRL,CAD-BRL,EUR-BRL')

        response.raise_for_status()

        data = response.json()

        moedas = {'moedas': [
            {
                'nome': data['USDBRL']['name'],
                'valor': data['USDBRL']['high'],
                'dtLeitura': data['USDBRL']['create_date']
            },
            {
                'nome': data['CADBRL']['name'],
                'valor': data['CADBRL']['high'],
                'dtLeitura': data['CADBRL']['create_date']
            },
            {
                'nome': data['EURBRL']['name'],
                'valor': data['EURBRL']['high'],
                'dtLeitura': data['EURBRL']['create_date']
            },
        ]}
        
        print('Cotações registradas!')
        es.index(index='moedas', id=str(uuid4()), document=moedas) 
    except Exception as e:
        print(f'Erro ao se comunicar com awesomeAPI: {e}')