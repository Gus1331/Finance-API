from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with, abort
from config import create_app

app = create_app()
api = Api(app)

app.run()