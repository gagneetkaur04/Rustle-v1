import os
class Config():
    SQLALCHEMY_DATABASE_URI = "sqlite:///rustle.db"
    SECRET_KEY = '789cb2387604bf1e9b603cc8b1924ef2'
    UPLOAD_FOLDER = './static/audios/'
    IMAGE_FOLDER = './static/pictures/'
    ADMIN_USERNAME = 'admin@a.com'
    ADMIN_PASSWORD = 'adminpassword'
    DEBUG = True