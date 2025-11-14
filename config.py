import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))


class Config:
    """
    Базовий клас конфігурації.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = 1 
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "data.db")
    )

class TestingConfig(Config):
    """
    Конфігурація для тестування.
    """
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """
    Конфігурація для продакшену.
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    
    'default': DevelopmentConfig
}
