from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from config import create_app
from config import conect_elastic
from uuid import uuid4

app = create_app()
es = conect_elastic(app)
api = Api(app)

## Controllers
class User(Resource):
    def post(self):
        data = request.get_json()  # Quando o corpo da requisição é JSON
        
        # Verificando se os campos necessários existem na requisição
        nome = data.get('nome')
        email = data.get('email')
        senha = data.get('senha')
        
        if not nome or not email or not senha:
            return {"message": "Todos os campos são obrigatórios!"}, 400
        
        busca = es.search(
            index="users", 
            body={
                "query": {
                    "match": {
                        "email": email
                    }
                }
            }
        )
        
        if(busca['hits']['total']['value'] > 0):
            return {"message": "Email já cadastrado!"}, 409
        
        
        user_id = str(uuid4())
        
        user_data = {
            "nome": nome,
            "email": email,
            "senha": senha
        }
        
        try:
            #es.index(index='users', id=user_id, document=user_data) 
            return jsonify({"message": "Usuário criado com sucesso!", "user_id": user_id})
        except Exception as e:
            return {"message": f"Erro ao inserir dados no Elasticsearch: {e}"}, 500

## Rotas

api.add_resource(User, '/users/')

app.run()