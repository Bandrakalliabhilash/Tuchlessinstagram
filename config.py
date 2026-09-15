import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_touchgram_secret")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}

ALLOWED_VIDEO_EXTENSIONS = {"mp4", "mov", "avi"}


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY", "touchgram_secret")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://root:Abhi@localhost/touchgram"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt_touchgram_secret")

    UPLOAD_FOLDER = UPLOAD_FOLDER

    ALLOWED_IMAGE_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS

    ALLOWED_VIDEO_EXTENSIONS = ALLOWED_VIDEO_EXTENSIONS