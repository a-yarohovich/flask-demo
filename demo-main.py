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



app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit_field = SubmitField('Submit')


@app.errorhandler(404)
def user_404(name):
    return render_template('404.html'), 404


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