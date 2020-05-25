import sqlite3
from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests



app = Flask(__name__)

api= Api(app)
db_path = "./database.db"

parser = reqparse.RequestParser()
parser.add_argument('sensor_ip')

# name: ip
sensors = {}

# meas_pi_url = "http://192.168.1.8:5000"
# GT11 = requests.get(meas_pi_url + "/sensorbyname/GT11").json()
# GT12 = requests.get(meas_pi_url + "/sensorbyname/GT12").json()

def request(sensor_name, ip):
    return requests.get("http://" + ip + "/sensorbyname/" + sensor_name, timeout=3).json()

def requestSensors(ip):
    return requests.get("http://" + ip + "/getdeclaredsensors/", timeout=3).json()


measurements = {}
#measurements["GT11"] = GT11
#measurements["GT12"] = GT12

class measurements_resources(Resource):
    def get(self, sensor_name):
        # return sensor_name
        try:
            return {sensor_name: request(sensor_name, sensors[sensor_name]["ip"])}
        except KeyError:
            return 'No sensors yet', 200
        except requests.exceptions.ConnectionError:
            return 'Cant connect to sensor', 400
        except requests.exceptions.Timeout:
            return 'Request timed out', 400

    def put(self, sensor_name):
        args = parser.parse_args()
        try: 
            if sensors[sensor_name]:
                return 'Sensor exists', 400
        except KeyError:
            pass
        sensors[sensor_name] = {"ip": args["sensor_ip"]}
        insertsensor((sensor_name, args['sensor_ip']))
        return '', 201

    def delete(self, sensor_name):
        # Remove sensor
        try:
            sensors[sensor_name]
        except KeyError:
            return 'Sensor doesnt exist', 400
        sensors.pop(sensor_name)
        removesensor((sensor_name))
        return '', 204

class ReadSensorsFromStation(Resource):
    def get(self):
        args = parser.parse_args()
        self.sensors = requestSensors(args["sensor_ip"])
        return self.sensors

api.add_resource(measurements_resources, "/<string:sensor_name>")
api.add_resource(ReadSensorsFromStation, "/readsensorsfromstation/")

def initdb(sensors):
    # Initialize database
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """CREATE TABLE IF NOT EXISTS sensors
        (name string,
        ip string);"""
        c.execute(q)
    sensors = initsensor(sensors)
    return sensors

def insertsensor(sensor_name_ip):
    # Insert sensor to DB
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """INSERT INTO sensors
        (name, ip)
        VALUES(?, ?) """
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
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """SELECT * FROM sensors"""
        c.execute(q)
        rows = c.fetchall()
    for row in rows:
        sensordict[row[0]] = {"ip" : row[1]}
    return sensordict

if __name__ == '__main__':
    sensors = initdb(sensors)
    app.run(debug=True, host="0.0.0.0")


