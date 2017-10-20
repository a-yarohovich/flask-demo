from flask import render_template, redirect, request, url_for, flash
from . import cbkwidget
from .forms import CbkWidgetForm

@cbkwidget.route('/cbkwidget', methods=['GET', 'POST'])
def create_cbkwidget():
    form = CbkWidgetForm()
    if form.validate_on_submit():
        target_adress = form.target_adress.data
        if target_adress is not None:
            flash("Congratulation!")
    return render_template('cbkwidget/cbkwidget.html', form=form)