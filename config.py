import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        "postgresql://postgres:public@localhost:25432/carpark"
        #'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL') or 'mqtt.netpie.io'
    MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT') or 1883
    MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID') or 'c9e27032-f75b-4fed-893c-92c199f5e491'
    MQTT_TOKEN = os.environ.get('MQTT_TOKEN') or 'T6(T3JvAGS&!ygw*v(t.X08@c0vm&JiS'
    UPLOAD_FOLDER = os.path.join(basedir, 'app/static/csv')
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
