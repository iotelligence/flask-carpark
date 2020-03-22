import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MODEL_FILE = os.environ.get('MODEL_FIE') or 'model.h5'
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL') or 'mqtt.netpie.io'
    MQTT_BROKER_PORT = os.environ.get('MQTT_BROKER_PORT') or 1883
    MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID') or None
    MQTT_TOKEN = os.environ.get('MQTT_TOKEN') or None
