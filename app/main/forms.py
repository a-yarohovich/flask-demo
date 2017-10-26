from flask_wtf import FlaskForm
from wtforms import *

class FsProfileForm(FlaskForm):
    sip_user_id = StringField('sip user id', [validators.DataRequired(message='Field is required')])
    sip_password = PasswordField('sip password', [validators.DataRequired(message='Field is required')])
    sip_display_name = StringField('sip display name')
    vm_password = PasswordField('voice mail password', [validators.DataRequired(message='Field is required')])
    outbound_caller_name = StringField('outbound caller name')
    outbound_caller_number = StringField('outbound caller number')
    submit = SubmitField('Register')
