from collections import defaultdict
from datetime import datetime
import json
from itertools import groupby
from threading import Thread
import time

from flask import request, url_for, render_template, Response
from flask_socketio import emit

import paho.mqtt.subscribe as subscribe

from app import app, db, socketio
from app.models import Carpark


thread = None


class Slot(object):
    def __init__(self, floor_slot):
        c = (
            Carpark.query.filter_by(floor_slot=floor_slot)
            .order_by(Carpark.timestamp.desc())
            .first()
        )
        self.floor_slot = floor_slot
        self.floor = floor_slot.split("_")[0]
        self.avail = "available" if c.available else "occupied"
        self.timestamp = c.timestamp


def _extract(mqtt_msg):
    msg = mqtt_msg
    board_no = msg.topic.split("/")[-1]
    json_str = str(msg.payload.decode("ascii")).replace("\x00", "")
    data = json.loads(json_str)

    return board_no, data["data"]


def carpark_thread():
    MQTT_BROKER_URL = app.config.get("MQTT_BROKER_URL")
    MQTT_BROKER_PORT = int(app.config.get("MQTT_BROKER_PORT"))
    CLIENT_ID = app.config.get("MQTT_CLIENT_ID")
    NETPIE_TOKEN = app.config.get("MQTT_TOKEN")
    while True:
        msg = subscribe.simple(
            "@msg/taist2020/board/#",
            hostname=MQTT_BROKER_URL,
            port=MQTT_BROKER_PORT,
            client_id=CLIENT_ID,
            auth={"username": NETPIE_TOKEN, "password": None},
            keepalive=600,
        )
        floor, avail = _extract(msg)
        data = Carpark(floor_slot=floor, available=avail == "available")
        db.session.add(data)
        db.session.commit()

        socketio.emit(
            "carpark response",
            {"floor": floor, "avail": avail, "last_update": str(data.timestamp)},
            namespace="/test",
        )


@app.route("/dashboard")
def dashboard():
    global thread
    if thread is None:
        thread = Thread(target=carpark_thread)
        thread.daemon = True
        thread.start()

    floor_slots = [
        i.floor_slot for i in db.session.query(Carpark.floor_slot).distinct()
    ]
    floor_groups = defaultdict(list)
    for floor_slot in floor_slots:
        floor_groups[floor_slot.split("_")[0]].append(Slot(floor_slot))

    devices = dict()
    for floor_slot in floor_slots:
        c = (
            Carpark.query.filter_by(floor_slot=floor_slot)
            .order_by(Carpark.timestamp.desc())
            .first()
        )
        available = "available" if c.available else "occupied"
        timestamp = c.timestamp
        devices[floor_slot] = [available, timestamp]

    return render_template("index.html", devices=devices, floor_groups=floor_groups)


@app.route("/export")
def generate_csv():
    def generate():
        results = Carpark.query.all()
        yield ",".join(Carpark.__table__.columns.keys()[1:]) + "\n"
        for row in results:
            floor_slot, available, timestamp = (
                row.floor_slot,
                "available" if row.available else "occupied",
                str(row.timestamp),
            )
            data = [floor_slot, available, timestamp]
            yield ",".join(data) + "\n"

    return Response(generate(), mimetype="text/csv")


@socketio.on("connect", namespace="/test")
def test_connect():
    emit("my connected", {"data": "Connected!!<br>Waiting for STM32 Boards"})


@socketio.on("disconnect", namespace="/test")
def test_disconnect():
    print("Client disconnected")
