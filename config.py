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

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.BREWLOCKER_MAIL_SENDER,
            toaddrs=[cls.BREWLOCKER_ADMIN],
            subject=cls.BREWLOCKER_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
