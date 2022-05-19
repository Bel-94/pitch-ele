import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://belinda:2015@localhost/pitch'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    SESSION_COOKIE_SECURE = False
    SECRET_KEY='Belminnyx'

    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL","")
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI =SQLALCHEMY_DATABASE_URI.replace("postgres://","postgresql://",)


class DevConfig(Config):
    
    DEBUG=True

config_options = {
'development':DevConfig,
'production':ProdConfig
}