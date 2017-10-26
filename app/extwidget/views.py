from flask import render_template, redirect, request, url_for, flash
from .forms import ExtWidgetForm
from . import extwidget


@extwidget.route('/ext', methods=['GET', 'POST'])
def call_me():
    form = ExtWidgetForm()
    if form.validate_on_submit():
        call_to = form.call_to.data
        if call_to is not None:
            return redirect('http://127.0.0.1:5000/login')
    return render_template('extwidget/ext.html', form=form)