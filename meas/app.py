import sqlite3
from flask import Flask
from flask_restful import Api, Resource, reqparse

import requests


app = Flask(__name__)

api= Api(app)
db_path = "../database.db"

parser = reqparse.RequestParser()
parser.add_argument('sensor_ip')

# name: ip
sensors = {}

# meas_pi_url = "http://192.168.1.8:5000"
# GT11 = requests.get(meas_pi_url + "/sensorbyname/GT11").json()
# GT12 = requests.get(meas_pi_url + "/sensorbyname/GT12").json()

def request(sensor_name, ip):
    return requests.get(ip + "/sensorbyname/" + sensor_name).json()

def requestSensors(ip):
    return requests.get(ip + "/getdeclaredsensors").json()


measurements = {}
measurements["GT11"] = GT11
measurements["GT12"] = GT12

class measurements_resources(Resource):
    def get(self, sensor_name):
        return {sensor_name: request(sensor_name, sensors[sensor_name]["ip"])}

    def put(self, sensor_name):
        args = parser.parse_args()
        sensors[sensor_name] = {"ip": args["sensor_ip"]}
        insertsensor((sensor_name, args['sensor_ip']))
        return '', 201

    def delete(self, sensor_name):
        # Remove sensor
        sensors.pop(sensor_name)
        removesensor((sensor_name))
        return '', 204

class ReadSensorsFromStation(Resource):
    def get(self, ip):



api.add_resource(measurements_resources, "/")


def initdb():
    # Initialize database
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """CREATE TABLE IF NOT EXISTS sensors
        (id int primary key,
        name string,
        ip string);"""
        c.execute(q)

def insertsensor(sensor_name_ip):
    # Insert sensor to DB
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """INSERT INTO sensors
        (name, ip)
        VALUES(?, ?)"""
        try:
            c.execute(q, sensor_name_ip)
            conn.commit()
        except sqlite3.IntegrityError as e:
            return e
        return False


def removesensor(sensor_name):
    # Remove sensor to DB
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """DELETE FROM sensors
        WHERE name = ?"""
        try:
            c.execute(q, (sensor_name,))
            conn.commit()
        except sqlite3.IntegrityError as e:
            return e
        return False

def initsensor(sensordict):
    # Populate sensors dict with values from db
    # First Initialize db
    initdb()
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """SELECT * FROM sensors"""
        c.execute(q)
        rows = c.fetchall()
    for row in rows:
        sensordict[row[1]] = {"ip" : row[2]}
    return sensordict
