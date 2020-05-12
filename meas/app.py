from flask import Flask
from flask_restful import Api, Resource

import requests


app = Flask(__name__)
api= Api(app)

meas_pi_url = "http://192.168.1.8:5000"
GT11 = requests.get(meas_pi_url + "/sensor/1").json()
# GT11 = requests.get("http://192.168.1.8:5000/sensor/2").json()
GT12 = requests.get(meas_pi_url + "/sensor/2").json()
# GT12 = requests.get("http://192.168.1.8:5000/sensor/2").json()

measurements = {}
measurements["GT11"] = GT11
measurements["GT12"] = GT12

class measurements_resources(Resource):
    def get(self ):
        return {"bla": measurements}

api.add_resource(measurements_resources, "/")

