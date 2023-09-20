import os
from app import app, db, errors
from app.forms import RSVPForm
from app.models import Guest
from app.email import send_email
from flask import flash, redirect, render_template, url_for

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome To Our Wedding')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():

    form = RSVPForm()

    if form.validate_on_submit():
        guest = Guest(
            attending = int(form.attending.data),
            name = form.name.data,
            email = form.email.data,
            phone = form.phone.data,
            diet_req = form.diet_req.data,
            message = form.message.data
        )

        diet_dict = {
            1: 'Vegetarian',
            2: 'Vegan',
            3: 'Nuts allergies',
            4: 'Fish and or shellfish allergies',
            5: 'Other'
        }

        if guest.diet_req:
            # Cast the chosen diet requirements into a string e.g. [1,3,4] -> '134'
            guest.diet_req = ''.join(map(str, guest.diet_req))
            # also create an readable string for the email confirmation.
            diet_string = ', '.join([diet_dict[int(i)] for i in ' '.join(guest.diet_req).split()])
        else:
            guest.diet_req = 0
            diet_string = 'None'

        # Send confirmation email of a sucessfull RSVP
        try:
            send_email(
                subject="NP LG Wedding RSVP confirmation",
                to_emails = guest.email,
                text_body = render_template('email/rsvp_response.txt', guest = guest, diet_string = diet_string),
                html_body = render_template('email/rsvp_response.html', guest = guest, diet_string = diet_string)
            )

        except Exception as err:
            flash(f'There was a problem submitting your RSVP. Please try again. If the problem persists please contact {app.config["ADMINS"][0]} - {err}', 'error')
            app.logger.error(f'Failed to send RSVP confirmation email to {guest.email} - {guest} - {err}')
            db.session.rollback()

        else:
            db.session.add(guest)
            db.session.commit()
            flash(f"Thank you! Your RSVP has been successfully submitted. You will shortly receive a confirmation email to {guest.email} (you may need to check your junk/spam folders).", 'message')
            app.logger.info(f'Successfully sent RSVP confirmation to {guest.email} - {guest}')

        return redirect(url_for('index'))

    return render_template('rsvp.html', title = "RSVP", form = form)


@app.route('/event-info')
def event_info():
    return render_template('event_info.html', title = 'Event Info')

@app.route('/faq')
def faq():
    return render_template('faq.html', title = 'FAQ')