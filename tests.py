from datetime import datetime
import unittest


from app import create_app, db
from app.models import Carpark
from config import Config

class TestConfig(Config):
    TESTING = True
    #using sqlite database for testing
    SQLALCHEMY_DATABASE_URI = "sqlite://"


class CarparkModelsTestCase(unittest.TestCase):
    """
    Tests model functionality.
    """

    def setUp(self):
        #start a temp service
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        #create a testing database
        db.create_all()

    def tearDown(self):
        #finish testing, drop the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_data_record(self):
        #getting the current time
        now = datetime.utcnow()
        #import the data by Carpark function
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
        #start a temp service
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        #create a testing database
        db.create_all()

    def tearDown(self):
        #finish testing, drop the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_dashboard_status_code(self):
        #get the response of the url https://servername/
        result = self.client.get("/")
        #check if the response status code is 200 or not
        self.assertEqual(result.status_code, 200)
        #get the response of the url https://servername/dashboard 
        result = self.client.get("/dashboard")
        #check if the response status code is 200 or not
        self.assertEqual(result.status_code, 200)


class ExportDataTestcase(unittest.TestCase):
    """
    Tests of export data.
    """

    def setUp(self):
        #start a temp service
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        #create a testing database
        db.create_all()
        
        #import the data to the sqlite database
        now = datetime.utcnow()
        car = Carpark(floor_slot="F2_3", available=False, timestamp=now)
        db.session.add(car)
        db.session.commit()
        
        #transfer the data from each column to csv format
        floor_slot = car.floor_slot
        available = "available" if car.available == True else "occupied"
        date = car.timestamp.strftime("%Y-%m-%d")
        time = car.timestamp.strftime("%H:%M:%S")
        self.expect = """Slot,Status,Date,Time\n{},{},{},{}\n""".format(
            floor_slot, available, date, time
        ).encode("utf-8")

    def tearDown(self):
        #finish testing, drop the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_export_status_code(self):
        #get the response of the url https://servername/export
        result = self.client.get("/export")
        #check if the response status code is 200 or not
        self.assertEqual(result.status_code, 200)

    def test_export_mimetype_csv(self):
        #get the response of the url https://servername/export
        result = self.client.get("/export")
        #check if the export file is in csv format
        self.assertEqual(result.mimetype, "text/csv")

    def test_export_csv_data(self):
        #get the response of the url https://servername/export
        result = self.client.get("/export")
        #check if the export file's data matchs with the import string
        self.assertEqual(result.data, self.expect)
                

class InsightTestcase(unittest.TestCase):
    """
    Tests of export data.
    """

    def setUp(self):
        #start a temp service
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        #create a testing database
        db.create_all()

    def tearDown(self):
        #finsh testing, drop the database
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_insights_status_code(self):
        #get the response of the url https://servername/insights
        result = self.client.get("/insights")
        #check if the response status code is 200 or not
        self.assertEqual(result.status_code, 200)



if __name__ == "__main__":
    unittest.main(verbosity=2)
