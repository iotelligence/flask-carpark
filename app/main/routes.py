from collections import defaultdict
from datetime import datetime
import json
import os
from threading import Thread
import time

from bokeh.embed import components
from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.resources import INLINE

from flask import redirect, request, url_for, render_template, Response, current_app, stream_with_context, flash
from flask_socketio import emit

import paho.mqtt.subscribe as subscribe
import pandas as pd

from werkzeug.utils import secure_filename

from app import db, socketio
from app.main import bp
from app.models import Carpark


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


def carpark_thread(app):
    with app.app_context():
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


@bp.before_app_first_request
def carpark_threadpool():
    thread = Thread(target=carpark_thread, args=(current_app._get_current_object(),))
    thread.daemon = True
    thread.start()


@bp.route("/")
@bp.route("/dashboard")
def dashboard():
    #global thread
    #if thread is None:
    #    thread = Thread(target=carpark_thread)
    #    thread.daemon = True
    #    thread.start()

    floor_slots = [
        i.floor_slot for i in db.session.query(Carpark.floor_slot).distinct()
    ]
    floor_slots.sort()

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

    return render_template("main/index.html", devices=devices, floor_groups=floor_groups)


@bp.route("/export")
def generate_csv():
    floor = request.args.get('floor') or request.args.get('f') or 'all'
    floor = floor.upper()
    def generate():
        CSV_COLUMNS = ['Slot', 'Status', 'Date', 'Time']
        if floor == 'ALL':
            results = Carpark.query.all()
        else:
            results = Carpark.query.filter(Carpark.floor_slot.startswith(floor+'_')).all()
        yield ",".join(CSV_COLUMNS) + "\n"
        for row in results:
            floor_slot, available, timestamp = (
                row.floor_slot,
                "available" if row.available else "occupied",
                row.timestamp,
            )

            date = timestamp.strftime("%Y-%m-%d")
            time = timestamp.strftime("%H:%M:%S")
            data = [floor_slot, available, date, time]
            yield ",".join(data) + "\n"

    response = Response(stream_with_context(generate()), mimetype="text/csv")
    filename = 'data_{}.csv'.format(floor) or 'data.csv'
    response.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response


@bp.route('/insights', methods=['GET', 'POST'])
def upload_file():
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = ['csv']
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main.upload_file',
                                    filename=filename))

    day_of_week = [
        "Monday",
        "Tuesday",
        "Wednsday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    results_weekday = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], "results_weekday.csv"), names=["weekday", "value"])

    list_of_hours = ["{}:00".format(h) for h in range(9, 22)]
    results_hourly = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], "results_hour.csv"))

    # init a basic bar chart:
    # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    fig = figure(
        x_range=day_of_week,
        title="% Average parking occupancy group by Day of Week",
        plot_width=600,
        plot_height=300,
        toolbar_location=None,
        x_axis_label="Day of week",
        y_axis_label="AVG % Occupancy",
    )
    fig.vbar(
        x=day_of_week,
        bottom=0,
        top=results_weekday["value"].to_list(),
        width=0.5,
        color="navy",
    )

    fig2 = figure(
        x_range=list_of_hours,
        title="% Average parking occupancy group by Hour",
        plot_width=600,
        plot_height=300,
        toolbar_location=None,
    )
    fig2.vbar(
        x=list_of_hours,
        bottom=0,
        top=results_hourly["percent_occupied"].to_list(),
        width=0.5,
        color="navy",
    )

    plots = [fig, fig2]

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    # script, div = components(fig)
    script, div = components(plots)
    html = render_template(
        "main/insights.html",
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html


@socketio.on("connect", namespace="/test")
def test_connect():
    emit("my connected", {"data": "Connected!!<br>Waiting for STM32 Boards"})


@socketio.on("disconnect", namespace="/test")
def test_disconnect():
    print("Client disconnected")
