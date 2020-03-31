# Flask Carpark

## Carpark monitoring system

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