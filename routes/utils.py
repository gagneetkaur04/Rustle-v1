import os, secrets, logging
from models import User, Song, Album
from app import login_manager, app
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Set the log level and log format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Get the logger for the current module
logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_fn)

    form_audio.save(audio_path)

    return audio_fn

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

# def generate_charts():
#     # Retrieve counts from the database
#     song_count = get_song_count()
#     creator_count = get_creator_count()
#     user_count = get_user_count()

#     # Data for the charts
#     data = {
#         'category': ['Songs', 'Creators', 'Users'],
#         'count': [song_count, creator_count, user_count]
#     }

#     # Create a DataFrame from the data
#     df = pd.DataFrame(data)

#     # Create bar chart using Matplotlib
#     fig, ax = plt.subplots()
#     df.plot(kind='bar', x='category', y='count', ax=ax)
#     ax.set_title('Counts')
#     ax.set_xlabel('Category')
#     ax.set_ylabel('Count')

#     # Save the chart to a bytes object
#     buffer = BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#     chart_data = base64.b64encode(buffer.read()).decode()

#     plt.close()  # Clear the plot

#     return chart_data
