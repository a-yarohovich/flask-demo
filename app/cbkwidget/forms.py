from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Length
from .. models import User

class CbkWidgetForm(FlaskForm):
    my_choices = [('1', 'VEHICLES'), ('2', 'Cars'), ('3', 'Bicycles')]
    name = StringField('Namesdsdssd', [validators.DataRequired(message='Name is required')])
    title = StringField('title', [validators.DataRequired(message='Subject is required')])
    text = TextAreaField('Text', [validators.DataRequired(message='Text is required')])
    phonenumber = StringField('Phone number')
    phoneview = BooleanField('Display phone number on site')
    price = StringField('Price', [validators.Regexp('\d',
            message='This is not an integer number, please see the example and try again'), validators.Optional()] )
    password = PasswordField('Password', [validators.Optional()])
    email = StringField('Email',
            [validators.DataRequired(message='Email is required'), validators.Email(message='Your email is invalid')])
    category = SelectField(choices = my_choices, default = '1')
