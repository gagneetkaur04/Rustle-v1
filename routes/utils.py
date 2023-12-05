import os, secrets, logging
from models import User, Song, Album
from app import login_manager, app
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from werkzeug.routing import BaseConverter

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

def get_song_count():
    songs = Song.query.all()
    return len(songs)

def get_creator_count():
    creators = User.query.filter_by(is_creator=True).filter_by(is_admin=False).all()
    return len(creators)

def get_user_count():
    users = User.query.filter_by(is_admin=False).all()
    return len(users)

def get_album_count():
    albums = Album.query.all()
    return len(albums) 

def song_charts():
    song_count = get_song_count()

    plt.figure(figsize=(8, 6))
    plt.hist(song_count, bins=20, alpha=0.7)
    plt.title('Songs Distribution')
    plt.xlabel('Songs')
    plt.ylabel('Frequency')
    
    plot_buffer = BytesIO()
    plt.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)

    plot_data = base64.b64encode(plot_buffer.read()).decode('utf-8')

    return plot_data