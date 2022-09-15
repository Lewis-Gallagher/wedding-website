from contextlib import redirect_stderr
from turtle import title
from flask import flash, redirect, render_template, url_for, request
from pkg_resources import register_finder
from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm, EmptyForm, PostForm
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@login_required
def index():
    form = RSVPForm()
    if form.validate_on_submit():
        guest = Guest(name = form.post.data, 
                      author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
