from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class RSVPForm(FlaskForm):
    name = StringField(label = 'Name', validators = [DataRequired()])
    email = StringField(label = 'Contact email', validators = (DataRequired(), Email()))
    phone = IntegerField(label = 'Contact phone number', validators = [DataRequired()])
    message = TextAreaField(label = 'Message', validators = [Length(max = 150)])
    submit = SubmitField(label = 'Submit')
    