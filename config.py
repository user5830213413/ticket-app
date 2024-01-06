from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

class Config:
    DEBUG = config.getboolean('App', 'DEBUG')
    JWT_SECRET_KEY = config.get('App', 'secret_key')
    SQLALCHEMY_DATABASE_URI = config.get('App', 'db')
    SQLALCHEMY_TRACK_MODIFICATIONS = config.getboolean('App', 'db_MODIFICATIONS')