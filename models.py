from database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(50), nullable = False)
    is_creator = db.Column(db.Boolean, nullable=False, default=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_blacklisted = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


class Album(db.Model):
    id = db.Column('album_id', db.Integer, primary_key=True)
    album_name = db.Column(db.String(50), nullable = False) 
    genre = db.Column(db.String(30))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_flagged = db.Column(db.Boolean, nullable=False)

    creator_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __init__(self, album_name, creator_id, genre, date_created):
        self.album_name = album_name
        self.creator_id = creator_id
        self.genre = genre
        self.date_created = date_created
        self.is_flagged = False


class Song(db.Model):
    id = db.Column('song_id', db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.album_id'), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)    
    song_title = db.Column(db.String(50), nullable = False) 
    song_path = db.Column(db.String, nullable = False) 
    lyrics = db.Column(db.String, nullable = False) 
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)

    playlists = db.relationship('Playlist', secondary='playlist_song', back_populates='songs')

    def __init__(self, album_id, creator_id, song_title, song_path, lyrics, date_created):
        self.album_id = album_id
        self.creator_id = creator_id
        self.song_title = song_title
        self.song_path = song_path
        self.lyrics = lyrics
        self.date_created = date_created
        self.is_flagged = False


class Playlist(db.Model):
    id = db.Column('playlist_id', db.Integer, primary_key=True)
    playlist_title = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    songs = db.relationship('Song', secondary='playlist_song', back_populates='playlists')


class Playlist_Song(db.Model):
    __tablename__ = 'playlist_song'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.playlist_id'), primary_key=True, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('song.song_id'), primary_key=True, nullable=False)


class Rating(db.Model):
    __tablename__ = 'ratings'
    user_id = db.Column(db.Integer,db.ForeignKey('user.user_id'),primary_key=True)
    song_id = db.Column(db.Integer,db.ForeignKey('song.song_id'),primary_key=True)
    rating = db.Column(db.Integer)

    def __init__(self, user_id, song_id, rating):
        self.user_id = user_id
        self.song_id = song_id
        self.rating = rating