from flask import Blueprint

extwidget = Blueprint('extwidget', __name__)

from . import views