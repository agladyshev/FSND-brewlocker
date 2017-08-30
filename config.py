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
    UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'uploads')
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id': '1849498792045942',
            'secret': 'd81f26d702a5173727066a0928e5f752'
        },
        'github': {
            'id': '88ce38d7ff8024328136',
            'secret': 'ef273943075636518d281268703d8ef8f54e9f9e'
        },
        'google': {
            'id': '433026741879-pji3tinhbp21el6tnv6b0u4btmnijr3q.apps.googleusercontent.com',
            'secret': 'bMi4fF_05yRr0DfSIeFbpk7p'
        }
    }
    BREWLOCKER_POSTS_PER_PAGE = 18
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
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
