import os, secrets, logging
from models import User
from app import login_manager, app

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