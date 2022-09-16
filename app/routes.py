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
    return render_template('rsvp.html', title = "RSVP", form = form)