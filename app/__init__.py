import os

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO


#app = Flask(__name__)
#app.config.from_object(Config)
#socketio = SocketIO(app)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app


#from app import routes, models
from app import models
