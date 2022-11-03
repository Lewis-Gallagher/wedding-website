from turtle import title
from app import app, db
from app.forms import RSVPForm
from app.models import Guest
from flask import flash, redirect, render_template, url_for, request

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    form = RSVPForm()
    if form.validate_on_submit():
        guest = Guest(
            attending = form.attending.data,
            name = form.name.data,
            email = form.email.data,
            phone = form.phone.data,
            diet_req = form.diet_req.data,
            message = form.message.data
        )

        # If guest has diet_req, turn the list into a concatenated string e.g. [1,3,5] into '135' otherwise None
        if guest.diet_req:
            guest.diet_req = ''.join(map(str, guest.diet_req))
        else:
            guest.diet_req = None

        db.session.add(guest)
        db.session.commit()

        flash('Thank you! You have successfully submitted your RSVP. You will shortly receive a confirmation email.')
        return redirect(url_for('index'))

    return render_template('rsvp.html', title = "RSVP", form = form)


@app.route('/our-story')
def our_story():
    return render_template('our_story.html', title = "Our Story")


@app.route('/event-info')
def event_info():
    return render_template('event_info.html', title = "Event Info")
