from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, TelField, RadioField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, StopValidation

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
    Iterating the field will produce subfields, allowing custom rendering of the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class MultiCheckboxAtLeastOne():
    def __init__(self, message=None):
        if not message:
            message = 'At least one option must be selected.'
        self.message = message

    def __call__(self, form, field):
        if len(field.data) == 0:
            raise StopValidation(self.message)


class RSVPForm(FlaskForm):
    attending = RadioField(
        label = "Will you be attending?",
        validators = [DataRequired()],
        choices = [(1, "Yes, I will be attending."), (0, "No, I will not be attending.")]
        )
    name = StringField(
        label = 'Full Name', 
        validators = [DataRequired()]
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
        choices = [
            (1, "Vegetarian"), 
            (2, "Vegan"), 
            (3, "Nut allergies"),
            (4, "Fish and shelfish allergies"), 
            (5, "Other - please specify below")
            ]
        )
    message = TextAreaField(
        label = 'Message', 
        validators = [Length(max = 150)]
        )
    submit = SubmitField(
        label = 'Submit'
        )
    