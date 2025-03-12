from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, abort
from elasticsearch import Elasticsearch
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    es = Elasticsearch(
        [
            {'host': app.config['ELASTICSEARCH_HOST'], 
            'port': app.config['ELASTICSEARCH_PORT'], 
            'scheme': 'http'}
        ], basic_auth=(app.config['ELASTIC_USERNAME'], app.config['ELASTIC_PASSWORD']))

    try:
        print(es.info())
    except Exception as e:
        print(f"Erro ao conectar ao Elasticsearch: {e}")
        exit(1)
        
    return app
