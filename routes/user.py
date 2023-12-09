from database import db
from flask import render_template, request, current_app as app, redirect, url_for, flash
from flask_login import current_user,login_required
from models import Song, Playlist, Album, User, Rating
from forms import PlaylistForm, EditPlaylistForm, AddToPlaylistForm, RatingForm
from app import app
from routes.utils import logger


# User Home Page
@app.route('/home_user', methods=['GET', 'POST'])
@login_required
def home_user():

    user = current_user
    latest_songs = db.session.query(User, Song, Album)\
        .join(Song, User.id == Song.creator_id)\
        .join(Album, Song.album_id == Album.id)\
        .order_by(Song.date_created.desc()).limit(5).all()
    
    latest_albums = db.session.query(User, Album)\
        .join(Album, User.id == Album.creator_id)\
        .filter(Album.album_name!='Singles')\
        .order_by(Album.date_created.desc()).limit(5).all()

    return render_template('home_user.html', user=user, latest_songs=latest_songs, latest_albums=latest_albums)


# All Songs
@app.route('/all_songs', methods=['GET', 'POST'])
@login_required
def all_songs():

    user = current_user
    songs = db.session.query(User, Song)\
        .join(Song, User.id == Song.creator_id)\
        .order_by(Song.date_created.desc()).all()

    return render_template('admin_songs.html', user=user, songs=songs)


# All Albums
@app.route('/all_albums', methods=['GET', 'POST'])
@login_required
def all_albums():

    user = current_user
    albums = Album.query.filter(Album.album_name!='Singles')\
            .order_by(Album.date_created.desc()).all()

    return render_template('admin_albums.html', user=user, albums=albums)


# Become Artist
@app.route('/become_artist', methods=['GET', 'POST'])
@login_required
def become_artist():
    
    user = current_user
    
    user.is_creator = True
    db.session.commit()

    flash('You are now a creator!', 'success')
    return redirect(url_for('creator_profile'))


# PLAY A SONG AND ADD TO PLAYLIST
@app.route('/play_song/<int:song_id>', methods=['GET', 'POST'])
@login_required
def play_song(song_id):

    music = Song.query.get_or_404(song_id)

    song = db.session.query(User, Song)\
        .join(Song, User.id == Song.creator_id)\
            .filter(Song.id == song_id).first()
    
    playlists = Playlist.query.filter_by(user_id=current_user.id).all()
    playlist_count = len(playlists)

    playlist_form = PlaylistForm()

    addsong_form=AddToPlaylistForm()
    playlist_choices = [(playlist.id, playlist.playlist_title) for playlist in Playlist.query.filter_by(user_id=current_user.id).all()]
    addsong_form.playlist.choices = playlist_choices

    rating_form = RatingForm()
    user_rating = Rating.query.filter_by(user_id=current_user.id, song_id=song_id).first()

    if addsong_form.validate_on_submit():
            
        playlist_id = addsong_form.playlist.data
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        playlist.songs.append(music)
        db.session.commit()

        flash('Your song have been added to the playlist!', 'success')
        return redirect(url_for('play_song', song_id=song_id))

    elif playlist_form.validate_on_submit():

        playlist = Playlist(playlist_title=playlist_form.playlist_title.data, user_id=current_user.id)
        playlist.songs.append(music)
        db.session.add(playlist)
        db.session.commit()

        flash('Your playlist has been created and song added to it!', 'success')
        return redirect(url_for('play_song', song_id=song_id))

    elif rating_form.validate_on_submit():
        rating = int(request.form['rating'])

        if user_rating:
            user_rating.rating = rating
        else:
            user_rating = Rating(user_id=current_user.id, song_id=song_id, rating=rating)
            db.session.add(user_rating)

        db.session.commit()
        flash('Your rating has been recorded!', 'success')
        return redirect(url_for('play_song', song_id=song_id)) 


    return render_template('play_song.html', 
                           song=song, 
                           addsong_form=addsong_form,
                           playlist_form=playlist_form,
                           rating_form=rating_form,
                           playlists=addsong_form.playlist.choices, 
                           playlist_count=playlist_count,
                           user_rating=user_rating)



# ...................................PLAYLIST ROUTES ......................................

# User Profile/Dashboard and Create Playist
@app.route('/user', methods=['GET', 'POST'])
@login_required
def user_profile():
    user = current_user
    form = PlaylistForm()


    if request.method == 'GET':
        playlists = Playlist.query.filter_by(user_id=user.id).all()
        size = len(playlists)

        return render_template('user_profile.html', user=user, playlists=playlists, form=form, size=size)
    
    elif request.method == 'POST':

        if form.validate_on_submit():

            playlist = Playlist(playlist_title=form.playlist_title.data, user_id=current_user.id)

            db.session.add(playlist)
            db.session.commit()

            logger.info('playlist: %s, user: %s ', form.playlist_title.data, current_user.id)

            flash('Your playlist has been created!', 'success')
            return redirect(url_for('user_profile'))
        
        return render_template('user_profile.html', form=form)
    

# Get Playlist ---> Update and Read Playlist 
@app.route('/user/playlist/<int:playlist_id>', methods=['GET', 'POST'])
@login_required
def get_playlist(playlist_id):

    user = current_user

    playlist = Playlist.query.get_or_404(playlist_id)

    edit_playlist_form = EditPlaylistForm(obj=playlist)
    songs = playlist.songs

    song_info = []
    for song in songs:
        artist_name = User.query.get(song.creator_id).username
        album_name = Album.query.get(song.album_id).album_name
        song_info.append({'song': song, 'artist_name': artist_name, 'album_name': album_name})

    if edit_playlist_form.validate_on_submit():

        playlist.playlist_title = edit_playlist_form.playlist_title.data
        db.session.commit()

        flash('Your playlist has been edited!', 'success')
        return redirect(url_for('get_playlist', playlist_id=playlist_id))


    return render_template('playlist.html', user=user, 
                                            playlist=playlist, 
                                            songs=song_info, 
                                            edit_playlist_form=edit_playlist_form)


# Delete Playlist --> To delete the playlist 
@app.route('/user/playlist/<int:playlist_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_playlist(playlist_id):
    
        playlist = Playlist.query.get_or_404(playlist_id)
        db.session.delete(playlist)
        db.session.commit()
    
        flash('Your playlist has been deleted!', 'success')
        return redirect(url_for('user_profile'))