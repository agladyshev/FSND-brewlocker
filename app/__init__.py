from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
import boto3
import botocore
from flask_uploads import UploadSet, IMAGES, configure_uploads

from config import config


# import extensions
moment = Moment()
db = SQLAlchemy()
mail = Mail()
csrf = CSRFProtect()
s3 = boto3.client('s3')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


images = UploadSet('images', IMAGES)


def create_app(config_name):
    # create app
    app = Flask(__name__)
    # configure app
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # initialize extensions
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # provide https support
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # set up local storage
    configure_uploads(app, (images))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
