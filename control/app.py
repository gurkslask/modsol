import time

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class pumpresource(Resource):
    def get(self):
        return {"pump 1": "RRun"}

api.add_resource(pumpresource, "/")

"""@app.route('/')
def hello():
    return "Hello world!"""

