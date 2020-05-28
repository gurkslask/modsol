import sqlite3
from flask import Flask
from flask_restful import Resource, Api, reqparse
from w1thermsensor import W1ThermSensor


app = Flask(__name__)

api = Api(app)
db_path = "../database.db"

parser = reqparse.RequestParser()
parser.add_argument('sensor_id')

# name: id
sensors = {}

class SensorByName(Resource):
    def get(self, sensor_name):
        # Get value from sensor
        try:
            return {sensor_name: W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sensors[sensor_name]['id']).get_temperature()}
        except KeyError:
            return "Sensor doesnt exist"

    def put(self, sensor_name ):
        # Name a sensor, id and name
        args = parser.parse_args()
        sensors[sensor_name] = {"id": args['sensor_id']}
        insertsensor((sensor_name, args['sensor_id']))
        return '', 201

    def delete(self, sensor_name):
        # Remove sensor
        sensors.pop(sensor_name)
        removesensor((sensor_name))
        return '', 204

class SensorById(Resource):
    def get(self, sensor_id):
        # Get value of sensor by supplying sensor id
        return W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sensor_id).get_temperature()


class SensorList(Resource):
    def get(self):
        # Get list of available sensors
        return [sensor.id for sensor in W1ThermSensor.get_available_sensors()]

class GetDeclaredSensors(Resource):
    def get(self):
        # Get list of declared sensors
        print(sensors)
        return [val for val in sensors.keys()]


api.add_resource(SensorByName, "/sensorbyname/<string:sensor_name>")
api.add_resource(SensorById, "/sensorbyid/<string:sensor_id>")
api.add_resource(SensorList, "/sensorlist/")
api.add_resource(GetDeclaredSensors, "/getdeclaredsensors/")

@app.route("/")
def home():
    return "/sensorbyname/<string:sensor_name><br>/sensorbyid/<string:sensor_id><br>/sensorlist/<br>/getdeclaredsensors/<br>"

def read_sensor(sensor_id):
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """SELECT * FROM sensors WHERE id = ?"""
        c.execute(q, sensor_id)
        row = c.fetchone()
    if row:
        return row[1]
    else:
        return 'nodata'

def initdb():
    # Initialize database
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """CREATE TABLE IF NOT EXISTS sensors
        (id int primary key,
        name string,
        sensor_id integer);"""
        c.execute(q)

def insertsensor(sensor_name_id):
    # Insert sensor to DB
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """INSERT INTO sensors
        (name, sensor_id)
        VALUES(?, ?)"""
        try:
            c.execute(q, sensor_name_id)
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
        print(row)
        sensordict[row[1]] = {"id" : row[2]}
    return sensordict

if __name__ == '__main__':
    initdb()
    initsensor(sensors)
    app.run(debug=True, host="0.0.0.0")
