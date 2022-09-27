from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, TelField, RadioField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class RSVPForm(FlaskForm):
    attending = RadioField(
        label = "Will you be attending?",
        validators = [DataRequired()],
        choices = ["Yes, I will be attending.", "No, I will not be attending."]
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
        label = 'Dietary Requirements',
        validators = [DataRequired()], 
        choices = [(0, "None"), (1, "Vegetarian"), (2, "Vegan"), (3, "Nut allergies"), 
                   (4, "Fish and shelfish allergies"), (5, "Other - Please specify")]
        )
    message = TextAreaField(
        label = 'Message', 
        validators = [Length(max = 150)]
        )
    submit = SubmitField(
        label = 'Submit'
        )
    