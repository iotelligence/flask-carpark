from datetime import datetime
import unittest
import csv
import sqlite3

from app import create_app, db
from app.models import Carpark
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class CarparkModelsTestCase(unittest.TestCase):
    """
    Tests model functionality.
    """

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
        car = Carpark(floor_slot="F2_3", available=False, timestamp=now)
        db.session.add(car)
        db.session.commit()

        # Model
        self.assertEqual(car.floor_slot, "F2_3")
        self.assertFalse(car.available)
        self.assertEqual(car.timestamp, now)

        # Actual data in database
        row = Carpark.query.order_by(Carpark.timestamp.desc()).first()
        self.assertEqual(row.floor_slot , car.floor_slot)
        self.assertFalse(row.available, car.available)
        self.assertEqual(row.timestamp, car.timestamp)


class DashboardPageTestCase(unittest.TestCase):
    """
    Tests of dashboard page.
    """

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
        result = self.client.get("/")
        self.assertEqual(result.status_code, 200)
        result = self.client.get("/dashboard")
        self.assertEqual(result.status_code, 200)


class ExportDataTestcase(unittest.TestCase):
    """
    Tests of export data.
    """

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        now = datetime.utcnow()
        car = Carpark(floor_slot="F2_3", available=False, timestamp=now)
        db.session.add(car)
        db.session.commit()

        floor_slot = car.floor_slot
        available = "available" if car.available == True else "occupied"
        date = car.timestamp.strftime("%Y-%m-%d")
        time = car.timestamp.strftime("%H:%M:%S")
        self.expect = """Slot,Status,Date,Time\n{},{},{},{}\n""".format(
            floor_slot, available, date, time
        ).encode("utf-8")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_export_status_code(self):
        result = self.client.get("/export")
        self.assertEqual(result.status_code, 200)

    def test_export_mimetype_csv(self):
        result = self.client.get("/export")
        self.assertEqual(result.mimetype, "text/csv")

    def test_export_csv_data(self):
        result = self.client.get("/export")
        self.assertEqual(result.data, self.expect)
        
    def test_check_csv_data(self) :
        result = self.client.get("/export")
        rows = csv.reader(Result)
        for row in rows:
            print(row)
        print(self.expect)        

class InsightTestcase(unittest.TestCase):
    """
    Tests of export data.
    """

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

    def test_insights_status_code(self):
        result = self.client.get("/insights")
        self.assertEqual(result.status_code, 200)


if __name__ == "__main__":
    unittest.main(verbosity=2)
