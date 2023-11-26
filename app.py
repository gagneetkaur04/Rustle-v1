from flask import Flask
from config import Config
from database import db
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()
bcrypt = Bcrypt()
login_manager.login_view = 'login'
# login_manager.login_message_category= 'info'

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context():
        db.create_all()

    return app
    
app = create_app()

if __name__ == "__main__":
    from routes import *
    from models import *
    app.run(debug=True)
