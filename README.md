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
