import os, secrets, logging
from models import User, Song, Album, Rating
from app import login_manager, app
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from werkzeug.routing import BaseConverter
from database import db

# FOR DEBUGGING PURPOSES
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
#......................................................................................................


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class NegativeFloatConverter(BaseConverter):
    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_fn)

    form_audio.save(audio_path)

    return audio_fn

def delete_audio(audio_fn):
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_fn)
    os.remove(audio_path)

def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.config['IMAGE_FOLDER'], image_fn)

    form_image.save(image_path)

    return image_fn

def delete_image(image_fn):
    image_path = os.path.join(app.config['IMAGE_FOLDER'], image_fn)
    os.remove(image_path)

def user_growth_chart():
    dates = User.query.with_entities(User.date_created).all()

    date = {}
    for i in range(len(dates)):
        date[dates[i][0].strftime('%b %d, %Y')] = User.query.with_entities(User.id).group_by(User.date_created).count() - 1
        

    plt.figure(figsize=(12, 6))
    plt.plot(date.keys(), date.values(), marker='o')
    plt.title('User Growth Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Users')
    plt.yticks(range(0, max(date.values())+1, 1))
    plt.xticks(rotation=30)
    plt.grid(True)
    return plt

def song_performance_chart():

    songs = Song.query.all()

    song_growth = {}
    for song in songs:
        song_growth[song.song_title] = Rating.query.filter_by(song_id=song.id).count()

    plt.figure(figsize=(15, 8))
    plt.bar(song_growth.keys(), song_growth.values(), color='skyblue')
    plt.title('Song Performance')
    plt.xlabel('Song')
    plt.ylabel('Rating')
    plt.yticks(range(0,6))
    plt.xticks(rotation=30)
    plt.grid(axis='y')
    return plt

def get_top_artists_data():
    artists_data = db.session.query(User.username, db.func.avg(Rating.rating).label('avg_rating')) \
        .join(Song, User.id == Song.creator_id) \
        .join(Rating, Song.id == Rating.song_id) \
        .group_by(User.id) \
        .order_by(db.desc('avg_rating')) \
        .limit(10) \
        .all()

    return artists_data

def top_artists_chart(artists_data):
    artist_names = [data[0] for data in artists_data]
    avg_ratings = [data[1] for data in artists_data]

    plt.figure(figsize=(10, 6))
    plt.barh(artist_names, avg_ratings, color='skyblue')
    plt.title('Top Artists Based on Average Rating')
    plt.xlabel('Average Rating')
    plt.ylabel('Artist')
    plt.grid(axis='x')
    plt.tight_layout()

    return plt

def get_artist_song_ratio_data():
    artists_data = db.session.query(User.username, db.func.count(Song.id).label('song_count')) \
        .join(Song, User.id == Song.creator_id) \
        .group_by(User.id) \
        .all()

    return artists_data

def create_artist_song_ratio_chart(artists_data):
    artist_names = [data[0] for data in artists_data]
    song_counts = [data[1] for data in artists_data]

    plt.figure(figsize=(8, 8))
    plt.pie(song_counts, labels=artist_names, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title('Artist-to-Song Ratio')
    
    return plt

def plot_to_base64(plt_obj):
    img = BytesIO()
    plt_obj.savefig(img, format='png')
    img.seek(0)
    img_str = base64.b64encode(img.getvalue()).decode()
    return f'data:image/png;base64,{img_str}'