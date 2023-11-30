from database import db
from flask import render_template, request, current_app as app, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from models import User
from forms import *
from app import bcrypt, app


# Welcome Page Route
@app.route("/", methods=['GET', 'POST'])
def welcome():
    if current_user.is_authenticated:
        return redirect(url_for('home_user'))
    
    return render_template('welcome.html')


# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_user'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}. You can now login now !', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_user'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_user'))
        else:
            flash('Login Unsuccessful. Please check your email, password or role', 'danger')

    return render_template('login.html', form=form)


# Logout User Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))


# Search Route
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    pass