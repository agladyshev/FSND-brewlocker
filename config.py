import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    S3_ENABLE = False
    CLOUDINARY = False
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
            'id': os.environ.get('FACEBOOK_ID'),
            'secret': os.environ.get('FACEBOOK_SECRET')
        },
        'github': {
            'id': os.environ.get('GITHUB_ID'),
            'secret': os.environ.get('GITHUB_SECRET')
        },
        'google': {
            'id': os.environ.get('GOOGLE_ID'),
            'secret': os.environ.get('GOOGLE_SECRET')
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


class HerokuConfig(ProductionConfig):

    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))
    S3_ENABLE = False
    S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
    S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    CLOUDINARY = True
    CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL")

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}
