import sqlite3


def create_table(db):
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
    q = """UPDATE sensors
    SET value = ? 
    WHERE id = ?;"""
    cursor = db.cursor()
    cursor.execute(q, sensor)
    db.commit()


if __name__ == '__main__':
    dbpath = "./database.db"
    conn = sqlite3.connect(dbpath)
    create_table(conn)
    update_values(conn, (42.42, 1))
