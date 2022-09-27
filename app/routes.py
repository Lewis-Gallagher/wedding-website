from turtle import title
from app import app
from app.forms import RSVPForm
from flask import flash, redirect, render_template, url_for, request

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/rsvp', methods=['GET', 'POST'])
def rsvp():
    form = RSVPForm()
    if form.validate_on_submit():
        redirect(url_for('index'))

    return render_template('rsvp.html', title = "RSVP", form = form)

@app.route('/our-story')
def our_story():
    return render_template('our_story.html', title = "Our Story")


@app.route('/event-info')
def event_info():
    return render_template('event_info.html', title = "Event Info")
