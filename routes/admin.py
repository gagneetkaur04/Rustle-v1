from database import db
from flask import render_template, current_app as app, redirect, url_for, flash
from flask_login import current_user,login_required
from models import Song, User, Album
from app import app
from routes.utils import get_song_count, get_creator_count, get_user_count, get_album_count

# >>>>>>>>>>>>>>>>>> ADMIN DASHBOARD <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    song_count = get_song_count()
    creator_count = get_creator_count()
    user_count = get_user_count()
    album_count = get_album_count()
    # song_data = song_charts()


    return render_template('admin.html', 
                           song_count=song_count, 
                            creator_count=creator_count, 
                            user_count=user_count, 
                            album_count=album_count)


# >>>>>>>>>>>>>>>>>> ADMIN USERS <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/users", methods=['GET', 'POST'])
@login_required
def admin_users():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    user_count = get_user_count()
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
    
    creator_count = get_creator_count()
    creators = User.query.filter_by(is_creator=True).filter_by(is_admin=False).all()

    return render_template('admin_creators.html', creators=creators, creator_count=creator_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE CREATOR <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/creators/<int:user_id>", methods=['GET', 'POST'])
@login_required
def admin_creator(user_id):
    user = User.query.get_or_404(user_id)
    songs = Song.query.filter_by(creator_id=user_id).all()
    albums = Album.query.filter_by(creator_id=user_id).all()

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

    for song in songs:
        db.session.delete(song)

    for album in albums:
        db.session.delete(album)

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

    if user.is_blacklisted:
        user.is_blacklisted = False
        db.session.commit()
        flash('User Whitelisted', 'success')
    else:
        user.is_blacklisted = True
        db.session.commit()
        flash('User Blacklisted', 'success')

    return redirect(url_for('admin_creator', user_id=user_id))


# >>>>>>>>>>>>>>>>>> ADMIN SONGS <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/songs", methods=['GET', 'POST'])
@login_required
def admin_songs():
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    song_count = get_song_count()
    songs = Song.query.all()
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

    if song.is_flagged:
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
    
    album_count = get_album_count()
    albums = Album.query.all()
    return render_template('admin_albums.html', albums=albums, album_count=album_count)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE ALBUM <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/albums/<int:album_id>", methods=['GET', 'POST'])
@login_required
def admin_album(album_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album = Album.query.get_or_404(album_id)
    songs = Song.query.filter_by(album_id=album_id).all()

    return render_template('admin_album.html', album=album, songs=songs)


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE ALBUM - DELETE <<<<<<<<<<<<<<<<<<<<<<< 
@app.route("/admin/albums/<int:album_id>/delete", methods=['GET', 'POST'])
@login_required
def admin_album_delete(album_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album = Album.query.get_or_404(album_id)
    songs = Song.query.filter_by(album_id=album_id).all()

    db.session.delete(songs)
    db.session.delete(album)
    db.session.commit()

    flash('Album deleted', 'success')
    return redirect(url_for('admin_albums'))


# >>>>>>>>>>>>>>>>>> ADMIN SINGLE ALBUM - FLAG <<<<<<<<<<<<<<<<<<<<<<<
@app.route("/admin/albums/<int:album_id>/flag", methods=['GET', 'POST'])
@login_required
def admin_album_flag(album_id):
    if not current_user.is_admin:
        return redirect(url_for('error'))
    
    album = Album.query.get_or_404(album_id)

    if album.is_flagged:
        album.is_flagged = False
        db.session.commit()
        flash('Album Unflagged', 'success')
    else:
        album.is_flagged = True
        db.session.commit()
        flash('Album Flagged', 'danger')
    return redirect(url_for('admin_album', album_id=album_id))
