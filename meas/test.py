import unittest
from app import app, sensors


class TestGetSensor(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get('/GT11')
        assert b'No sensors yet' in response.data

        response = self.app.put('/GT11', json={"sensor_ip": "192.168.1.8"})
        assert response.status_code == 201

        response = self.app.put('/GT11', json={"sensor_ip": "192.168.1.8"})
        assert response.status_code == 400
        assert b'Sensor exists' in response.data

        response = self.app.get('/GT11')
        assert b'Cant connect to sensor' in response.data

        response = self.app.delete('/GT11')
        assert response.status_code == 204

        response = self.app.delete('/GT11')
        assert response.status_code == 400
        assert b'Sensor doesnt exist' in response.data 

if __name__ == '__main__':
    unittest.main()

