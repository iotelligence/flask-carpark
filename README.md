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
$ python3 -m virtualenv --python=python3 venv
$ sourve venv

# Start here
(venv) $ git clone https://github.com/phondanai/flask-carpark
(venv) $ cd flask-carpark
(venv) $ pip install -r requirements.txt
(venv) $ flask db upgrade
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
```
$ git push heroku master
```
