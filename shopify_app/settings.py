import os


class Config(object):

    DEBUG = False
    TESTING = False

    SECRET_KEY = os.environ.get('CONDUIT_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PREFERRED_URL_SCHEME = 'https'

    SHOPIFY_API_KEY = '5aedc5bc79f1ac9ea8bf45c8b786cec2'
    SHOPIFY_SHARED_SECRET = 'f7b4a5856490a7355107167c4d462281'
    SHOPIFY_API_VERSION = '2020-01'


class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/example')


class DevConfig(Config):
    """Development configuration."""

    ENV = 'dev'
    DEBUG = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True
