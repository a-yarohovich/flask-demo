import os

from datetime import datetime

from flask import Flask
from flask import make_response
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session, flash

from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_script import Manager

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import *

from flaskext.mysql import MySQL
from flask import request

mysql = MySQL()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '00hnb98A'
app.config['MYSQL_DATABASE_DB'] = 'demo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit_field = SubmitField('Submit')


@app.errorhandler(404)
def user_404(name):
    return render_template('404.html'), 404

@app.route("/auth")
def authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    result = "Username or Password is wrong" if data is None else "Logged in successfully"
    return render_template('auth.html', auth_result=result)


@app.route('/', methods=('GET', 'POST'))
def index():
    mform = MyForm()
    if mform.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != mform.name.data:
            flash('Looks like you have changed your name')
        session['name'] = mform.name.data
        mform.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=mform,
                           name=session.get('name'))


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    return render_template('userform.html', form=form)


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    manager.run()