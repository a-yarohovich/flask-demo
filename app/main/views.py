from flask import render_template, session, redirect, url_for, current_app
from .. import db
from ..email import send_email
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        username = form.name.data
        cursor = db.connect().cursor()
        cursor.execute("select * from users where username='" + username + "'")
        data = cursor.fetchone()
        db_user = None
        if data is not None:
            db_user = data[1]

        if db_user is None:
            user = username
            session['known'] = False
            #send_email(current_app.config['ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))