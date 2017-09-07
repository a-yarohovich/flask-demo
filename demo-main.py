from datetime import datetime

from flask import Flask
from flask import make_response
from flask import render_template

from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_script import Manager

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


@app.errorhandler(404)
def user_404(name):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    return render_template('userform.html', form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()