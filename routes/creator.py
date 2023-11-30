from database import db
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user,login_required
from models import Song, Album
from forms import *
from app import app
from routes.utils import save_audio, logger


# Creator Profile ; Add Album ;  Add Song
@app.route('/creator', methods=['GET', 'POST'])
@login_required
def creator_profile():

    if not current_user.is_creator:
        return redirect(url_for('error'))

    user = current_user
    album_form = AlbumForm()
    song_form = SongForm()

    albums = [(album.id, album.album_name) for album in Album.query.filter_by(creator_id=user.id).all()]
    albums.insert(0, (-1, 'Singles'))
    song_form.album.choices = albums

    if request.method == 'GET':
        albums = Album.query.filter_by(creator_id=user.id).all()
        songs = Song.query.filter_by(creator_id=user.id).all()

        album_size = len(albums)
        songs_size = len(songs)

        return render_template('creator_profile.html', user=user, albums=albums, 
                                    songs=songs, album_form=album_form, 
                                    song_form=song_form, album_size=album_size, 
                                    songs_size=songs_size)

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


# ................................... ALBUMS ROUTES ......................................

# Get album ---> To view the songs in the album ; Edit Album
@app.route('/album/<int:album_id>', methods=['GET', 'POST'])
@login_required
def get_album(album_id):

    if not current_user.is_creator:
        return redirect(url_for('error'))

    album= Album.query.filter_by(id=album_id).first()
    songs = Song.query.filter_by(album_id=album_id).all()

    editAlbumForm = EditAlbumForm(obj=album)

    if request.method == 'POST':

        if editAlbumForm.validate_on_submit():

            album.album_name = editAlbumForm.album_title.data
            album.genre = editAlbumForm.genre.data

            db.session.commit()

            flash('Your album has been edited!', 'success')
            return redirect(url_for('get_album', album_id=album_id))

    editAlbumForm.album_title.data = album.album_name
    return render_template('album.html', user=current_user, songs=songs, album=album, editAlbumForm=editAlbumForm)

# Delete album --> To delete the album
@app.route('/album/<int:album_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_album(album_id):

    if not current_user.is_creator:
        return redirect(url_for('error'))
        
    album = Album.query.filter_by(id=album_id).first()
    db.session.delete(album)
    db.session.commit()

    flash('Your album has been deleted!', 'success')
    return redirect(url_for('creator_profile'))


# ................................... SONGS ROUTES ......................................

# Get song ---> To view the songs; EDIT SONG
@app.route('/song/<int:song_id>', methods=['GET'])
@login_required
def get_song(song_id):

    if not current_user.is_creator:
        return redirect(url_for('error'))
    
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

    return render_template('song.html', user=current_user, song=song, form=form)

# Delete song --> To delete the song
@app.route('/song/<int:song_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_song(song_id):

    if not current_user.is_creator:
        return redirect(url_for('error'))
        
    song = Song.query.filter_by(id=song_id).first()
    db.session.delete(song)
    db.session.commit()

    flash('Your song has been deleted!', 'success')
    return redirect(url_for('creator_profile'))