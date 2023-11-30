from flask_wtf import FlaskForm
from models import User
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
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
    playlist_title = StringField('Title', validators=[DataRequired()])
    
    submit = SubmitField('Create Playlist')

class EditPlaylistForm(FlaskForm):
    playlist_title = StringField('Title', validators=[DataRequired()])
    
    submit = SubmitField('Update')


class AlbumForm(FlaskForm):
    album_title = StringField('Album Title', validators=[DataRequired()])
    genre = StringField('Genre')

    submit = SubmitField('Create Album')

class EditAlbumForm(FlaskForm):
    album_title = StringField('Album Title', validators=[DataRequired()])
    genre = StringField('Genre')

    submit = SubmitField('Update')


class SongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired()])
    lyrics = TextAreaField('Lyrics', validators=[DataRequired()])
    duration = StringField('Song Duration', validators=[DataRequired()])
    album = SelectField('Select Album', coerce=int)
    audio_file = FileField('Audio File', validators=[DataRequired()])

    submit = SubmitField('Create Song')

    def validate_file(self, audio_file):
        allowed_extensions = ['mp3']
        if audio_file.data:
            file_ext = audio_file.data.filename.rsplit('.', 1)[1].lower()
            if file_ext not in allowed_extensions:
                raise ValidationError('File must be in MP3 format')

class EditSongForm(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired()])
    lyrics = TextAreaField('Lyrics', validators=[DataRequired()])
    duration = StringField('Song Duration', validators=[DataRequired()])
    album = SelectField('Select Album', coerce=int)

    submit = SubmitField('Update')


class AddToPlaylistForm(FlaskForm):
    playlist = SelectField('Playlist', coerce=int)
    submit = SubmitField('Add to Playlist')



class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')