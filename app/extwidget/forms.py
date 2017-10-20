from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ExtWidgetForm(FlaskForm):
    call_to = StringField('+xxxxxxx', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('call me')