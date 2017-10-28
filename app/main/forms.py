from flask_wtf import FlaskForm
from wtforms import *

class FsProfileForm(FlaskForm):
    sip_user_id = StringField('sip user id', [validators.DataRequired(message='Field is required')])
    sip_password = PasswordField('sip password', [validators.DataRequired(message='Field is required')])
    sip_display_name = StringField('sip display name')
    vm_password = PasswordField('voice mail password', [validators.DataRequired(message='Field is required')])
    outbound_caller_name = StringField('outbound caller name')
    outbound_caller_number = StringField('outbound caller number')
    is_default_profile = BooleanField('Mark as default profile')
    submit = SubmitField('Register')

"""    from flask_wtf import FlaskForm
    from wtforms import *
    from wtforms.validators import DataRequired, Length
    from ..models import User
    class CbkWidgetForm(FlaskForm):
    my_choices = [('1', 'VEHICLES'), ('2', 'Cars'), ('3', 'Bicycles')]

    name = StringField('Namesdsdssd', [validators.DataRequired(message='Name is required')])
    title = StringField('title', [validators.DataRequired(message='Subject is required')])
    text = TextAreaField('Text', [validators.DataRequired(message='Text is required')])
    phonenumber = StringField('Phone number')
    phoneview = BooleanField('Display phone number on site')
    price = StringField('Price', 
                        [validators.Regexp('\d', message = 'This is not an integer number, please see the example and try again'), validators.Optional()] )
    password = PasswordField('Password', [validators.Optional()])
    email = StringField('Email', [validators.DataRequired(message='Email is required'), validators.Email(message='Your email is invalid')])
    category = SelectField(choices=my_choices, default='1')
"""