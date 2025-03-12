from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, abort
from elasticsearch import Elasticsearch

username = 'elastic'
password = 'nY5AQz37ZZIfMev9nY5AQz37ZZIfMev9'

es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}], basic_auth=(username, password))

# Teste de conexão
print(es.info())

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# api = Api(app)