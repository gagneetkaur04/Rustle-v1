from database import db
from flask import render_template, request, current_app as app, redirect, url_for, flash
from flask_login import current_user,login_required
from models import Song, Playlist
from forms import PlaylistForm, EditPlaylistForm, AddToPlaylistForm
from app import app
from routes.utils import logger


# Become Artist
@app.route('/become_artist', methods=['GET', 'POST'])
@login_required
def become_artist():
    
    user = current_user
    
    user.is_creator = True
    db.session.commit()

    flash('You are now a creator!', 'success')
    return redirect(url_for('creator_profile'))



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
    # addsong_form=AddSongToPlaylistForm()

    playlist = Playlist.query.filter_by(id=playlist_id).first()
    edit_playlist_form = EditPlaylistForm(obj=playlist)

    playlist = Playlist.query.filter_by(id=playlist_id).first()
    songs = playlist.songs

    # addsong_form.selected_song.choices = [(song.id, song.song_title) for song in Song.query.all()]

    # if addsong_form.validate_on_submit():
    #     selected_song = addsong_form.selected_song.data
    #     playlist_id = playlist.id

    #     for song_id in selected_song:
    #         song = Song.query.filter_by(id=song_id).first()
    #         playlist.songs.append(song)
    #         db.session.commit()

    #     flash('Your song have been added to the playlist!', 'success')
    #     return redirect(url_for('get_playlist', playlist_id=playlist_id))


    if edit_playlist_form.validate_on_submit():

        playlist.playlist_title = edit_playlist_form.playlist_title.data
        db.session.commit()

        flash('Your playlist has been edited!', 'success')
        return redirect(url_for('get_playlist', playlist_id=playlist_id))



    return render_template('playlist.html', user=user, 
                                            playlist=playlist, 
                                            songs=songs, 
                                            edit_playlist_form=edit_playlist_form)


# Delete Playlist --> To delete the playlist 
@app.route('/user/playlist/<int:playlist_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_playlist(playlist_id):
    
        playlist = Playlist.query.filter_by(id=playlist_id).first()
        db.session.delete(playlist)
        db.session.commit()
    
        flash('Your playlist has been deleted!', 'success')
        return redirect(url_for('user_profile'))


# PLAY A SONG AND ADD TO PLAYLIST
@app.route('/play_song/<int:song_id>', methods=['GET', 'POST'])
@login_required
def play_song(song_id):

    form=AddToPlaylistForm()
    song = Song.query.get_or_404(song_id)
    return render_template('play_song.html', song=song, form=form)