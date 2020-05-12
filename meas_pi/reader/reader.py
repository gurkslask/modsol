import sqlite3
from w1thermsensor import W1ThermSensor
import time


def create_table(db):
    # Initiates a table and 2 rows
    q = """CREATE TABLE IF NOT EXISTS sensors 
    (id int primary key,
    value float,
    name string);"""
    cursor = db.cursor()
    cursor.execute(q)

    #Populate with rows
    q = """INSERT INTO sensors
    VALUES( 1, 0, "GT11");"""
    cursor = db.cursor()
    try:
        cursor.execute(q)
    except sqlite3.IntegrityError as e:
        print(e)
    db.commit()

    q = """INSERT INTO sensors
    VALUES(2, 0, "GT12");"""
    cursor = db.cursor()
    try:
        cursor.execute(q)
    except sqlite3.IntegrityError as e:
        print(e)
    db.commit()

def update_values(db, sensor):
    # Updates values of sensor
    q = """UPDATE sensors
    SET value = ? 
    WHERE id = ?;"""
    cursor = db.cursor()
    cursor.execute(q, sensor)
    db.commit()

def read_sensor(sensor_id):
    # Reads temperature of a DS1820 temp sensor
    sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, sensor_id)
    return sensor.get_temperature()


if __name__ == '__main__':
    dbpath = "../database.db"
    sensor1_id = "000005237c0f"
    sensor2_id = "0000052a8428"
    conn = sqlite3.connect(dbpath)
    with conn:
        create_table(conn)
        while True:
            # Update every minute
            sensor1_temp = read_sensor(sensor1_id)
            update_values(conn, (sensor1_temp, 1))
            sensor2_temp = read_sensor(sensor2_id)
            update_values(conn, (sensor2_temp, 2))
            time.sleep(60)
