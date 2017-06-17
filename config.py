import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    BREWLOCKER_MAIL_SUBJECT_PREFIX = '[BrewLocker]'
    BREWLOCKER_MAIL_SENDER = 'BrewLocker Admin'
    BREWLOCKER_ADMIN = os.environ.get('BREWLOCKER_ADMIN')
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '111262736058256',
            'secret': 'e79921d4781bedbd7dade8811ab32f9b'
        },
        'twitter': {
            'id': 'oMG4NWeOFb5Yy6NUUeXtt5WTd',
            'secret': 'DK36BohrTXrOfLgIXsc0T7l5VfWleFY2io6m6YMrJ794h9Qm7R'
        },
        'google': {
            'id': '312958319092-t72jvbratej6v1aac1cr4efg6sboj753.apps.googleusercontent.com',
            'secret': 'LqJmuY3-s7A8q5vW1pTAH3wu'
        }
    }
    @staticmethod
    # configuration-specific initialization
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
