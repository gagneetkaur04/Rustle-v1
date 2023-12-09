from database import db
from flask import render_template, current_app as app, redirect, url_for, flash
from flask_login import current_user,login_required
from models import Song, User, Album, Playlist, Rating
from app import app
from routes.utils import NegativeFloatConverter, delete_audio, user_growth_chart
from routes.utils import plot_to_base64, song_performance_chart, top_artists_chart, get_top_artists_data, get_artist_song_ratio_data, create_artist_song_ratio_chart

app.url_map.converters['negfloat'] = NegativeFloatConverter

# >>>>>>>>>>>>>>>>>> ADMIN DASHBOARD <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin_dashboard():

    num_users = User.query.filter_by(is_admin=False).count()
    num_songs = Song.query.count()
    num_creators = User.query.filter_by(is_creator=True).filter_by(is_admin=False).count()
    num_albums = Album.query.filter(Album.album_name != 'Singles').count()

    avg_rating = db.session.query(db.func.round(db.func.avg(Rating.rating), 2)).scalar()
    artists_data = get_top_artists_data()
    artist_songs_data = get_artist_song_ratio_data()

    user_growth_chart_b64 = plot_to_base64(user_growth_chart())
    song_performance_chart_b64 = plot_to_base64(song_performance_chart())
    top_artists_chart_b64 = plot_to_base64(top_artists_chart(artists_data))
    artist_song_ratio_chart_b64 = plot_to_base64(create_artist_song_ratio_chart(artist_songs_data))


    return render_template('admin.html', 
                           num_users=num_users,
                           num_songs=num_songs,
                           num_creators=num_creators,
                           num_albums=num_albums,
                           avg_rating=avg_rating,
                           user_growth_chart=user_growth_chart_b64,
                           top_artists_chart=top_artists_chart_b64,
                           song_performance_chart=song_performance_chart_b64,
                           artist_song_ratio_chart=artist_song_ratio_chart_b64)


# >>>>>>>>>>>>>>>>>> ADMIN USERS <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/users", methods=['GET', 'POST'])
@login_required
def admin_users():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    user_count = User.query.filter_by(is_admin=False).count()
    users = User.query.filter_by(is_admin=False).all()

    return render_template('admin_users.html', users=users, user_count=user_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE USER <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/users/<int:user_id>", methods=['GET', 'POST'])
@login_required
def admin_user(user_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    user = User.query.get_or_404(user_id)

    return render_template('admin_user.html', user=user)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE USER - DELETE <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/users/<int:user_id>/delete", methods=['GET', 'POST'])
@login_required
def admin_user_delete(user_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    user = User.query.get_or_404(user_id)
    playlists = Playlist.query.filter_by(user_id=user_id).all()
    rating = Rating.query.filter_by(user_id=user_id).all()

    for playlist in playlists:
        db.session.delete(playlist)

    if user.is_creator:
        songs = Song.query.filter_by(creator_id=user_id).all()
        albums = Album.query.filter_by(creator_id=user_id).all()

        for song in songs:
            rating = Rating.query.filter_by(song_id=song.id).all()
            for rate in rating:
                db.session.delete(rate)

            delete_audio(song.song_path)
            db.session.delete(song)

        for album in albums:
            db.session.delete(album)
    

    for rate in rating:
        db.session.delete(rate)

    db.session.delete(user)
    db.session.commit()
    flash('User deleted', 'success')
    return redirect(url_for('admin_users'))


# >>>>>>>>>>>>>>>>>> ADMIN CREATORS <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/creators", methods=['GET', 'POST'])
@login_required
def admin_creators():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    creator_count = User.query.filter_by(is_creator=True).filter_by(is_admin=False).count()
    creators = User.query.filter_by(is_creator=True).filter_by(is_admin=False).all()

    return render_template('admin_creators.html', creators=creators, creator_count=creator_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE CREATOR <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/creators/<int:user_id>", methods=['GET', 'POST'])
@login_required
def admin_creator(user_id):
    user = User.query.get_or_404(user_id)
    songs = Song.query.filter_by(creator_id=user_id).all()
    albums = Album.query.filter_by(creator_id=user_id).filter(Album.album_name != 'Singles').all()

    song_count = len(songs)
    album_count = len(albums)

    return render_template('admin_creator.html', user=user, songs=songs, albums=albums, song_count=song_count, album_count=album_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE CREATOR - DELETE <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/creators/<int:user_id>/delete", methods=['GET', 'POST'])
@login_required
def admin_creator_delete(user_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    user = User.query.get_or_404(user_id)
    songs = Song.query.filter_by(creator_id=user_id).all()
    albums = Album.query.filter_by(creator_id=user_id).all()
    rating = Rating.query.filter_by(user_id=user_id).all()

    for song in songs:
        rating = Rating.query.filter_by(song_id=song.id).all()
        for rate in rating:
            db.session.delete(rate)

        delete_audio(song.song_path)
        db.session.delete(song)

    for album in albums:
        db.session.delete(album)

    for rate in rating:
        db.session.delete(rate)

    db.session.delete(user)
    db.session.commit()

    flash('Creator deleted', 'success')
    return redirect(url_for('admin_creators'))


# >>>>>>>>>>>>>>>>>> ADMIN CREATOR - BLACKLIST <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/creators/<int:user_id>/blacklist", methods=['GET', 'POST'])
@login_required
def admin_creator_blacklist(user_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    user = User.query.get_or_404(user_id)
    albums = Album.query.filter_by(creator_id=user_id).all()
    songs = Song.query.filter_by(creator_id=user_id).all()

    if user.is_blacklisted:
        user.is_blacklisted = False

        for album in albums:
            album.is_flagged = False
        
        for song in songs:
            song.is_flagged = False

        db.session.commit()
        flash('User Whitelisted', 'success')
    else:
        user.is_blacklisted = True

        for album in albums:
            album.is_flagged = True

        for song in songs:
            song.is_flagged = True

        db.session.commit()
        flash('User Blacklisted', 'success')

    return redirect(url_for('admin_creator', user_id=user_id))


# >>>>>>>>>>>>>>>>>> ADMIN SONGS <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/songs", methods=['GET', 'POST'])
@login_required
def admin_songs():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    song_count = Song.query.count()
    songs = db.session.query(User, Song)\
        .join(Song, User.id == Song.creator_id).all()

    return render_template('admin_songs.html', songs=songs, song_count=song_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE SONG <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/songs/<int:song_id>", methods=['GET', 'POST'])
@login_required
def admin_song(song_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    song = db.session.query(User, Song)\
    .join(Song, User.id == Song.creator_id)\
        .filter(Song.id == song_id).first()
    
    return render_template('admin_song.html', song=song)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE SONG - DELETE <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/songs/<int:song_id>/delete", methods=['GET', 'POST'])
@login_required
def admin_song_delete(song_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    song = Song.query.get_or_404(song_id)
    rating = Rating.query.filter_by(song_id=song_id).all()
    for rate in rating:
        db.session.delete(rate)

    delete_audio(song.song_path)
    db.session.delete(song)
    db.session.commit()
    flash('Song deleted', 'success')

    return redirect(url_for('admin_songs'))


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE SONG - FLAG <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/songs/<int:song_id>/flag", methods=['GET', 'POST'])
@login_required
def admin_song_flag(song_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    song = Song.query.get_or_404(song_id)
    artist = User.query.get(song.creator_id)

    if song.is_flagged:

        if artist.is_blacklisted:
            flash('Artist is blacklisted. Song cannot be unflagged. You need to whitelist the artist first.', 'danger')

        else:
            song.is_flagged = False
            db.session.commit()
            flash('Song Unflagged', 'success')

    else:
        song.is_flagged = True
        db.session.commit()
        flash('Song Flagged', 'danger')

    return redirect(url_for('admin_song', song_id=song_id))


# >>>>>>>>>>>>>>>>>> ADMIN ALBUMS <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/albums", methods=['GET', 'POST'])
@login_required
def admin_albums():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album_count = Album.query.filter(Album.album_name != 'Singles').count()
    albums = Album.query.filter(Album.album_name != 'Singles').all()

    return render_template('admin_albums.html', albums=albums, album_count=album_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE ALBUM <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/albums/<negfloat:album_id>", methods=['GET', 'POST'])
@login_required
def admin_album(album_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album = Album.query.get_or_404(album_id)
    songs = Song.query.filter_by(album_id=album_id).all()
    artist = User.query.get(album.creator_id).username

    return render_template('admin_album.html', album=album, songs=songs, artist=artist)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE ALBUM - DELETE <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/albums/<negfloat:album_id>/delete", methods=['GET', 'POST'])
@login_required
def admin_album_delete(album_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album = Album.query.get_or_404(album_id)
    songs = Song.query.filter_by(album_id=album_id).all()
    
    for song in songs:
        rating = Rating.query.filter_by(song_id=song.id).all()
        for rate in rating:
            db.session.delete(rate)
            
        delete_audio(song.song_path)
        db.session.delete(song)
        db.session.commit()

    db.session.delete(album)
    db.session.commit()

    flash('Album deleted', 'success')
    return redirect(url_for('admin_albums'))


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE ALBUM - FLAG <<<<<<<<<<<<<<<<<<<<<<<
@app.route("/admin/albums/<negfloat:album_id>/flag", methods=['GET', 'POST'])
@login_required
def admin_album_flag(album_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album = Album.query.get_or_404(album_id)
    songs = Song.query.filter_by(album_id=album_id).all()
    artist = User.query.get(album.creator_id)

    if album.is_flagged:

        if artist.is_blacklisted:
            flash('Artist is blacklisted. Album cannot be unflagged. You need to whitelist the artist first.', 'danger')

        else:
            album.is_flagged = False

            for song in songs:
                song.is_flagged = False

            db.session.commit()
            flash('Album Unflagged', 'success')
    else:
        album.is_flagged = True

        for song in songs:
            song.is_flagged = True

        db.session.commit()
        flash('Album Flagged', 'danger')

    return redirect(url_for('admin_album', album_id=album_id))
