from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TelField, RadioField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from app.models import Guest

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
    Iterating the field will produce subfields, allowing custom rendering of the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RSVPForm(FlaskForm):
    attending = RadioField(
        label = "Will you be attending?",
        validators = [DataRequired()],
        choices = [
            (1, "Yes, I will be attending."), 
            (0, "No, I will not be attending.")
            ]
        )
    name = StringField(
        label = 'Full Name', 
        validators = [DataRequired()],
        )
    email = StringField(
        label = 'Contact email', 
        validators = (DataRequired(), Email())
        )
    phone = TelField(
        label = 'Contact phone number', 
        validators = [DataRequired()]
        )
    diet_req = MultiCheckboxField(
        label = 'Dietary requirements', 
        validators = [Optional()],
        coerce = int,
        choices = [
            (1, "Vegetarian"), 
            (2, "Vegan"), 
            (3, "Nut allergies"),
            (4, "Fish and/or shelfish allergies"), 
            (5, "Other - please specify below")
            ]
        )
    message = TextAreaField(
        label = 'Message', 
        validators = [Length(max = 150)]
        )
    submit = SubmitField(
        label = 'RSVP'
        )
    
    def validate_email(self, email):
        email = Guest.query.filter_by(email=email.data).first()
        if email is not None:
            message = 'An RSVP under this email has already been submitted.'
            raise ValidationError(message)

    def validate_name(self, name):
        name = Guest.query.filter_by(name=name.data).first()
        if name is not None:
            message = 'An RSVP under this name has already been submitted.'
            raise ValidationError(message)
