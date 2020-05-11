import sqlite3
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)
db_path = "../database.db"

class sensor(Resource):
    def get(self, sensor_id):
        return{sensor_id: read_sensor(sensor_id)}

def read_sensor(sensor_id):
    conn = sqlite3.connect(db_path)
    with conn:
        c = conn.cursor()
        q = """SELECT * FROM sensors WHERE id = ?"""
        c.execute(q, sensor_id)
        row = c.fetchone()
    return row[1]

api.add_resource(sensor, "/<string:sensor_id>")

if __name__ == '__main__':
    print(read_sensor("1"))
