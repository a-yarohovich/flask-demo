from flask import render_template
from . import main_blueprint

@main_blueprint.app_errorhandler(404)
def user_404(name):
    return render_template('404.html'), 404


@app.errorhandler(500)
def user_404(name):
    return render_template('404.html'), 500