from flask_wtf import FlaskForm
from models import User
from wtforms import StringField, PasswordField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email() ])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])    
    
    submit = SubmitField('Login')


class PlaylistForm(FlaskForm):
    playlist_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    
    submit = SubmitField('Create Playlist')

class EditPlaylistForm(FlaskForm):
    playlist_title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    
    submit = SubmitField('Update')


class AlbumForm(FlaskForm):
    album_title = StringField('Album Title', validators=[DataRequired(), Length(min=2, max=20)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Create Album')

class EditAlbumForm(FlaskForm):
    album_title = StringField('Album Title', validators=[DataRequired(), Length(min=2, max=20)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=2, max=20)])

    submit = SubmitField('Update')


class SongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired(), Length(min=2, max=20)])
    lyrics = TextAreaField('Lyrics', validators=[DataRequired()])
    duration = StringField('Song Duration', validators=[DataRequired(), Length(min=2, max=20)])

    # albums = [('album_1', 'Album 1'), ('album_2', 'Album 2')]
    # album = RadioField('Album  ', choices=albums)

    submit = SubmitField('Create Song')

class EditSongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired(), Length(min=2, max=20)])
    lyrics = TextAreaField('Lyrics', validators=[DataRequired()])
    duration = StringField('Song Duration', validators=[DataRequired(), Length(min=2, max=20)])

    # albums = [('album_1', 'Album 1'), ('album_2', 'Album 2')]
    # album = RadioField('Album  ', choices=albums)

    submit = SubmitField('Update')