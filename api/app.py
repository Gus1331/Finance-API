from flask import Flask, request, jsonify, abort
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from config import create_app
from config import conect_elastic
from uuid import uuid4
from datetime import datetime, date

app = create_app()
es = conect_elastic(app)
api = Api(app)
jwt = JWTManager(app)


## Controllers
class User(Resource):
    def post(self):
        data = request.get_json()
        
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        
        if not nome or not email or not senha:
            abort(400)
        
        busca = es.search(
            index='users', 
            body={
                'query': {
                    'match': {
                        'email': email
                    }
                }
            }
        )
        
        print(busca['hits']['hits'][0]['_source'].get('email'))
        if(busca['hits']['total']['value'] > 0):
            return {'message': 'Email já cadastrado!'}, 409
        
        user_id = str(uuid4())
        
        user_data = {
            'nome': nome,
            'email': email,
            'senha': senha
        }
        
        try:
            #es.index(index='users', id=user_id, document=user_data) 
            return jsonify({'message': 'Usuário criado com sucesso!', 'user_id': user_id})
        except Exception as e:
            return {'message': f'Erro ao inserir dados no Elasticsearch: {e}'}, 500
        
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        email = data.get('email')
        senha = data.get('senha')

        if not email or not senha:
            abort(400)
        
        busca = es.search(
            index='users', 
            body={
                'query': {
                    'bool': {
                        'must': [
                            {'match': {'email': email}},
                            {'match': {'senha': senha}}
                        ]
                    }
                }
            }
        )

        if(busca['hits']['total']['value'] < 1 or busca['hits']['hits'][0]['_source'].get('email') != email or busca['hits']['hits'][0]['_source'].get('senha') != senha):
            return {'message': 'Credencias inválidas!'}, 401

        token = create_access_token(identity=busca['hits']['hits'][0]['_id'])

        return {'auth': token, 'message': 'Login bem sucedido!'}, 200
    
class FonteReceita(Resource):
    @jwt_required() 
    def post(self):
        data = request.get_json()

        nome = data.get('nome')
        fixo = data.get('fixo')

        if not isinstance(nome, str) or not isinstance(fixo, bool):
            abort(400)

        current_user = get_jwt_identity()

        font_receita = {
            'user': current_user,
            'nome': nome,
            'fixo': fixo,
            'dtRegistro': datetime.now()
        }

        try:
            entityId = str(uuid4())
            es.index(index='fontes_receitas', id=entityId, document=font_receita)
            font_receita['_id'] = entityId
            return jsonify(font_receita)
        except Exception as e:
            return {'message': f'Erro ao inserir dados no Elasticsearch: {e}'}, 500
        
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        busca = es.search(
            index='fontes_receitas', 
            body={
                'query': {
                    'match': {
                        'user': current_user
                    }
                }
            }
        )
        if(busca['hits']['total']['value'] < 1):
            return '', 204
        
        return jsonify(busca['hits']['hits'])
    
class TipoDespesa(Resource):
    @jwt_required() 
    def post(self):
        data = request.get_json()

        nome = data.get('nome')
        fixo = data.get('fixo')

        if not isinstance(nome, str) or not isinstance(fixo, bool):
            abort(400)

        current_user = get_jwt_identity()

        tipo_despesa = {
            'user': current_user,
            'nome': nome,
            'fixo': fixo,
            'dtRegistro': datetime.now()
        }

        try:
            entityId = str(uuid4())
            es.index(index='tipos_despesas', id=entityId, document=tipo_despesa)
            tipo_despesa['_id'] = entityId
            return jsonify(tipo_despesa)
        except Exception as e:
            return {'message': f'Erro ao inserir dados no Elasticsearch: {e}'}, 500
        
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        busca = es.search(
            index='tipos_despesas', 
            body={
                'query': {
                    'match': {
                        'user': current_user
                    }
                }
            }
        )
        if(busca['hits']['total']['value'] < 1):
            return '', 204
        
        return jsonify(busca['hits']['hits'])
    
class Receitas(Resource):
    @jwt_required() 
    def post(self):
        data = request.get_json()

        valor = data.get('valor')
        fonteId = data.get('fonteId')
        dtReceita = data.get('dtRaceita')

        if not isinstance(dtReceita, str) or not isinstance(valor, float) or not(fonteId, str):
            abort(400)

        try:
            dtReceita = date.fromisoformat(dtReceita)
        except Exception as e:
            print(f'Erro convertendo string para data: {e}')
            abort(400)

        current_user = get_jwt_identity()

        receita = {
            'user': current_user,
            'valor': valor,
            'fonteId': fonteId,
            'dtReceita': dtReceita,
            'dtRegistro': datetime.now()
        }

        try:
            entityId = str(uuid4())
            es.index(index='receitas', id=entityId, document=receita)
            receita['_id'] = entityId
            return jsonify(receita)
        except Exception as e:
            return {'message': f'Erro ao inserir dados no Elasticsearch: {e}'}, 500
        
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        busca = es.search(
            index='receitas', 
            body={
                'query': {
                    'match': {
                        'user': current_user
                    }
                }
            }
        )
        if(busca['hits']['total']['value'] < 1):
            return '', 204
        
        return jsonify(busca['hits']['hits'])

## Rotas

api.add_resource(User, '/users/')
api.add_resource(Login, '/login')
api.add_resource(Receitas , '/receitas')
api.add_resource(FonteReceita, '/receitas/fontes')
api.add_resource(TipoDespesa, '/despesas/tipos')
#api.add_resource(Despesas, '/despesas')

if __name__ == '__main__':
    app.run(debug=True)