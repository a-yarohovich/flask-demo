from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flaskext.mysql import MySQL
from core_config import config
from flask import Blueprint

bootstrap = Bootstrap()
moment = Moment()
mysql = MySQL()
main_blueprint = Blueprint('main', __name__)

from . import views, errors

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    mysql.init_app(app)

    app.register_blueprint(main_blueprint)

    return app