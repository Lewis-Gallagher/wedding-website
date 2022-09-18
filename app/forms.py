from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, TelField, RadioField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class RSVPForm(FlaskForm):
    attending = RadioField(label = "Will you be attending?", choices = ["Yes, I will be attending", "No, I will not be attending"])
    name = StringField(label = 'Name', validators = [DataRequired()])
    email = StringField(label = 'Contact email', validators = (DataRequired(), Email()))
    phone = TelField(label = 'Contact phone number', validators = [DataRequired()])
    message = TextAreaField(label = 'Message', validators = [Length(max = 150)])
    submit = SubmitField(label = 'Submit')
    