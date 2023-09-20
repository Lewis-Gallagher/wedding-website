from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, TelField, RadioField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from app.models import Guest
from markupsafe import Markup
from wtforms import SelectMultipleField, widgets
from markupsafe import Markup
 
 
class BootstrapListWidget(widgets.ListWidget):
 
    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(f"<li class='list-group-item'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
            else:
                html.append(f"<li class='list-group-item'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))
 
 
class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
 
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = BootstrapListWidget(prefix_label=False)
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
        label = 'Dietary requirements (if any)', 
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
        label = 'An optional message', 
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
