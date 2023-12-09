from database import db
from flask import render_template, request, current_app as app, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from models import User, Song, Album, Rating
from forms import RegistrationForm, LoginForm
from app import bcrypt, app


# Welcome Page Route
@app.route("/", methods=['GET', 'POST'])
def welcome():

    if not User.query.filter_by(email=app.config['ADMIN_EMAIL']).first():
        user = User(username=app.config['ADMIN_USERNAME'],
                    email=app.config['ADMIN_EMAIL'],
                    password=app.config['ADMIN_PASSWORD'])
        user.is_admin = True
        db.session.add(user)
        db.session.commit()

    if current_user.is_authenticated:
        if not current_user.is_admin:
            return redirect(url_for('home_user'))
        else:
            return redirect(url_for('admin_dashboard'))

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
    if current_user.is_authenticated and not current_user.is_admin:
        return redirect(url_for('home_user'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if form.email.data == app.config['ADMIN_EMAIL'] and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))

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
    
    query = request.args.get('q')

    # Search for songs
    songs = Song.query.join(User)\
             .filter(Song.song_title.ilike(f'%{query}%') | User.username.ilike(f'%{query}%'))\
             .all()
    
    # Search for albums
    albums = Album.query.join(User)\
             .filter(Album.album_name.ilike(f'%{query}%') | User.username.ilike(f'%{query}%'))\
             .all()
    
    flag_song_count = 0
    for song in songs:
        if song.is_flagged:
            flag_song_count += 1

    flag_album_count = 0
    for album in albums:
        if album.is_flagged:
            flag_album_count += 1

    album_size = len(albums)
    song_size = len(songs)
    

    # Format the results
    song_results = [{'id': song.id, 'title': song.song_title, 'artist': User.query.get(song.creator_id).username, 'flagged': song.is_flagged} for song in songs]
    album_results = [{'id': album.id, 'name': album.album_name, 'genre': album.genre, 'artist': User.query.get(album.creator_id).username} for album in albums]

    return render_template('search.html', 
                           query=query, 
                           songs=song_results, 
                           albums=album_results, 
                           album_size=album_size,
                           song_size=song_size,
                           flag_song_count=flag_song_count,
                           flag_album_count=flag_album_count)


# Error Page
@app.route("/error", methods=['GET', 'POST'])
def error():
    return render_template('error.html')