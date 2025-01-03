import os

class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///photography.db'
    UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')