import os

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'


class DevelopmentConfig(Config):
    DEBUG = True
    # Development-specific configuration options...

class ProductionConfig(Config):
    DEBUG = False
    # Production-specific configuration options...
