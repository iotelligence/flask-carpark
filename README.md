# Flask Carpark

Carpark monitoring system

## Requirements
```
Flask
Flask-Migrate
Flask-SocketIO
Flask-SQLAlchemy
eventlet
psycopg2
gunicorn
python-dotenv
paho-mqtt
SQLAlchemy
```

## Installation

```
# This step is optional if you're not prefered virtualenv
$ python3 -m pip install virtualenv # in case you don't have
$ python3 -m virtualenv --python=python3 venv
$ sourve venv

# Start here
(venv) $ git clone https://github.com/phondanai/flask-carpark
(venv) $ cd flask-carpark
(venv) $ pip install -r requirements.txt
(venv) $ flask db upgrade
```

## Configuration
Create `.env` file and create your own configuration
```
SECRET_KEY="youneverknow"
SQLALCHEMY_DATABASE_URI=""
MQTT_BROKER_URL="mqtt.netpie.io"
MQTT_BROKER_PORT=1883
MQTT_CLIENT_ID="your mqtt client id"
MQTT_TOKEN="your mqtt token"
```

## Run
```
(venv) $ gunicorn --worker-class eventlet -w 1 application:app
```

## Running test
```
$ python tests.py
```

## Deploy
You need [Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql).
And config your environment variable according to your `.env` file.
```
$ heroku config:set SECRET_KEY="youneverknow"
$ heroku config:set MQTT_BROKER_URL="mqtt.netpie.io"
$ # ... and so on
```

Then deploy
```
$ git push heroku master
```

## Data Analytic Testcase

Test case: Check_Generated_Data-001
Description: Check whether the generated data is exist or can be download and readable from data source. 

Prerequisites: 
      1. User Authorization
      2. Web-page Avaliable 

Test Procedure:
      1. Enter website 
      2. Show report data

Test data: Generated Data from database 

Expected results:The report of data should be appeared in web page 

Actual result: -

**************************************************************************************************************

Test case: Test_Format-001

Description:Validation of the data type,data length and schema format associated with this format

---------------------------------------------------------
           |               |                 |             
Floor_Slot |	Status       |	YYYY-MM-DD     |	  Time
-----------|---------------|-----------------|-----------
F3_22	     |   Occupied	   |  1/12/2020      |	 9:58:00
F2_10	     |   Available   |	1/13/2020      |	10:58:00
  
Prerequisites:
        1. User Authorization
        2. Web-page Avaliable

Test Procedure:
        1.Enter website
        2.Query data from website
        3.Validate format and data type whether they are correctly mapped or compatible with the specified format.

Test data: Generated Data from database 

Expected results the data type and format of table should compatible with the format 

Actual result: -

*************************************************************************************************************
# Parking Map
```
    Test case ID: Check the number of car had parking in each slots.
```
## Objective 
```
    To check the changing status of slots over a selected time period.
    The changing status : Available to Occupied parking.
```
## Procedure
```
    1. To load data.
    2. To select time period and the result should be show the number of changing status. 
    3. To check the result of counting method with the raw data. 
```
## Expected result
```
  When you selected time period such as 1.00 - 3.00 pm. 
  The result should be show number of changing status of slot.
  Therefore, we know the number of car that parked in here.
```
*************************************************************************************************************
