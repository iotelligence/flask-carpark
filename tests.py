from datetime import datetime
import unittest

from app import create_app, db
from app.models import Carpark
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class CarparkModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_data_record(self):
        now = datetime.utcnow()
        car = Carpark(floor_slot='F2_3', available=False, timestamp=now)
        db.session.add(car)
        db.session.commit()
        self.assertEqual(car.floor_slot, 'F2_3')
        self.assertFalse(car.available)
        self.assertEqual(car.timestamp, now)

class DashboardPageTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dashboard_status_code(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

        result = self.client.get('/dashboard')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=2)
