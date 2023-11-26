import logging, os, secrets
from config import Config
from database import db
from datetime import datetime
from flask import render_template, request, current_app as app, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from models import User, Song, Playlist, Album
from forms import RegistrationForm, LoginForm, PlaylistForm, AlbumForm, SongForm, EditPlaylistForm, EditAlbumForm, EditSongForm
from werkzeug.utils import secure_filename
from app import login_manager, bcrypt, app

# Set the log level and log format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Get the logger for the current module
logger = logging.getLogger(__name__)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> UTILS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_fn)

    form_audio.save(audio_path)

    return audio_path

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ROUTES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

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
        
        print(user.__dict__)

        db.session.add(user)
        db.session.commit()

        print("After db",user.__dict__)

        flash(f'Account created for {form.username.data}. You can now login now !', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_user'))  ## CHANGE NEEDED IN REDIRECTION
    
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


# ####################################################### USER ROUTES #########################################################


# User Home Page
@app.route('/home_user', methods=['GET', 'POST'])
@login_required
def home_user():

    user = current_user

    latest_songs = Song.query.order_by(Song.date_created.desc()).limit(10).all()

    return render_template('home_user.html', user=user, latest_songs=latest_songs)
    

# Become Artist
@app.route('/become_artist', methods=['GET', 'POST'])
@login_required
def become_artist():
    
    user = current_user
    
    user.is_creator = True
    db.session.commit()

    flash('You are now a creator!', 'success')
    return redirect(url_for('creator_profile'))



# ................................... USER PLAYLIST ROUTES ......................................

# User Profile/Dashboard and Create Playist
@app.route('/user', methods=['GET', 'POST'])
@login_required
def user_profile():
    user = current_user
    form = PlaylistForm()

    if request.method == 'GET':
        playlists = Playlist.query.filter_by(user_id=user.id).all()

        return render_template('user_profile.html', user=user, playlists=playlists, form=form)
    
    elif request.method == 'POST':

        if form.validate_on_submit():

            playlist = Playlist(playlist_title=form.playlist_title.data, user_id=current_user.id)

            db.session.add(playlist)
            db.session.commit()

            logger.info('playlist: %s, user: %s ', form.playlist_title.data, current_user.id)

            flash('Your playlist has been created!', 'success')
            return redirect(url_for('user_profile'))
        
        return render_template('user_profile.html', form=form)
    
# Get Playlist ---> To view the songs in the playlist
@app.route('/user/playlist/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def get_playlist(playlist_id):

    user = current_user

    if request.method == 'GET':

        playlist = Playlist.query.filter_by(id=playlist_id).first()
        songs = playlist.songs

        return render_template('playlist.html', user=user, playlist=playlist, songs=songs)

# Update Playlist --> To edit the name of the playlist
@app.route('/user/playlist/<int:playlist_id>/update', methods=['GET', 'POST'])
@login_required
def edit_playlist(playlist_id):

    playlist = Playlist.query.filter_by(id=playlist_id).first()

    form = EditPlaylistForm(obj=playlist)

    if form.validate_on_submit():

        playlist.playlist_title = form.playlist_title.data
        db.session.commit()

        flash('Your playlist has been edited!', 'success')
        return redirect(url_for('get_playlist', playlist_id=playlist_id))
        
    return render_template('playlist_edit.html', form=form)

# Delete Playlist --> To delete the playlist
@app.route('/user/playlist/<int:playlist_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_playlist(playlist_id):
    
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        db.session.delete(playlist)
        db.session.commit()
    
        flash('Your playlist has been deleted!', 'success')
        return redirect(url_for('user_profile'))
    



# ####################################################### CREATOR ROUTES #########################################################

# Creator Profile ; Add Album ;  Add Song
@app.route('/creator', methods=['GET', 'POST'])
@login_required
def creator_profile():

    user = current_user
    album_form = AlbumForm()
    song_form = SongForm()

    albums = [(album.id, album.album_name) for album in Album.query.filter_by(creator_id=user.id).all()]
    albums.insert(0, (-1, 'Singles'))
    song_form.album.choices = albums

    if request.method == 'GET':
        albums = Album.query.filter_by(creator_id=user.id).all()
        songs = Song.query.filter_by(creator_id=user.id).all()

        return render_template('creator_profile.html', user=user, albums=albums, songs=songs, album_form=album_form, song_form=song_form)

    elif request.method == 'POST':

        if album_form.validate_on_submit():

            album = Album(
                album_name=album_form.album_title.data,
                genre=album_form.genre.data,
                creator_id=current_user.id,
                date_created=datetime.now()
            )

            logger.info('album: %s, user: %s ', album_form.album_title.data, current_user.id)
            print(album)

            db.session.add(album)
            db.session.commit()
            flash('Your album has been created!', 'success')
            return redirect(url_for('creator_profile'))
        
        elif song_form.validate_on_submit():

            if song_form.audio_file.data:
                audio_path = save_audio(song_form.audio_file.data)

            song = Song(album_id=song_form.album.data,
                        creator_id=current_user.id,
                        song_title=song_form.song_title.data,
                        song_path=audio_path,
                        lyrics=song_form.lyrics.data,
                        duration=song_form.duration.data,
                        date_created=datetime.now())
            
            db.session.add(song)
            db.session.commit()

            logger.info('song: %s, user: %s ', song_form.song_title.data, current_user.id)

            flash('Your song has been added!', 'success')
            return redirect(url_for('creator_profile', _anchor='tabtwo'))


    return render_template('creator_profile.html', album_form=album_form, user=user, song_form=song_form)


# ................................... CREATOR ALBUM ROUTES ......................................

# Get album ---> To view the songs in the album
@app.route('/album/<int:album_id>', methods=['GET'])
@login_required
def get_album(album_id):

    album= Album.query.filter_by(id=album_id).first()
    songs = Song.query.filter_by(album_id=album_id).all()

    return render_template('album.html', user=current_user, songs=songs, album=album)

# Update album --> To edit the name of the album
@app.route('/album/<int:album_id>/update', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):

    album = Album.query.get_or_404(album_id)

    form = EditAlbumForm(obj=album)

    if form.validate_on_submit():

        album.album_name = form.album_title.data
        album.genre = form.genre.data

        db.session.commit()

        flash('Your album has been edited!', 'success')
        return redirect(url_for('get_album', album_id=album_id))
    
    form.album_title.data = album.album_name
    return render_template('album_edit.html', form=form)   

# Delete album --> To delete the album
@app.route('/album/<int:album_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_album(album_id):
        
    album = Album.query.filter_by(id=album_id).first()
    db.session.delete(album)
    db.session.commit()

    flash('Your album has been deleted!', 'success')
    return redirect(url_for('creator_profile'))


# ................................... CREATOR SONGS ROUTES ......................................

# Get song ---> To view the songs
@app.route('/song/<int:song_id>', methods=['GET'])
@login_required
def get_song(song_id):
    
    song = db.session.query(Song, User.username).join(User, Song.creator_id == User.id).filter(Song.id == song_id).first()
    return render_template('song.html', user=current_user, song=song[0], creator=song[1])

# Update song --> To edit the name of the song
@app.route('/song/<int:song_id>/update', methods=['GET', 'POST'])
@login_required
def edit_song(song_id):
        
    song = Song.query.filter_by(id=song_id).first()

    form = EditSongForm(obj=song)

    albums = [(album.id, album.album_name) for album in Album.query.filter_by(creator_id=current_user.id).all()]
    albums.insert(0, (-1, 'Singles'))
    form.album.choices = albums

    if form.validate_on_submit():

        song.song_title = form.song_title.data
        song.lyrics = form.lyrics.data
        song.duration = form.duration.data
        song.album_id = form.album.data

        db.session.commit()

        flash('Your song has been edited!', 'success')
        return redirect(url_for('get_song', song_id=song_id))
        
    return render_template('song_edit.html', form=form)

# Delete song --> To delete the song
@app.route('/song/<int:song_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_song(song_id):
        
    song = Song.query.filter_by(id=song_id).first()
    db.session.delete(song)
    db.session.commit()

    flash('Your song has been deleted!', 'success')
    return redirect(url_for('creator_profile'))





# ####################################################### ADMIN ROUTES #########################################################
