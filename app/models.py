from datetime import datetime
from . import db, login_manager, images as images_set
from .helpers import uploadToS3
from flask_login import UserMixin, AnonymousUserMixin, current_user
from flask import current_app, url_for, flash
import os
import glob
import json


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        # to create and update roles
        roles = {
            'User': (Permission.VIEW_CONTACTS |
                     Permission.COMMENT |
                     Permission.ADD_ITEMS, True),
            'Moderator': (Permission.VIEW_CONTACTS |
                          Permission.COMMENT |
                          Permission.ADD_ITEMS |
                          Permission.MODERATE, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class Permission:
    VIEW_CONTACTS = 0x01
    COMMENT = 0x02
    ADD_ITEMS = 0x04
    MODERATE = 0x08
    ADMINISTER = 0x80


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(64), index=True, nullable=False)
    provider_id = db.Column(db.String(64), unique=True,
                            index=True, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    items = db.relationship('Item', backref='author', lazy='dynamic')
    images = db.relationship('Image', backref='author', lazy='dynamic')

    @staticmethod
    def generate_fake(count=5):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     provider_id='facebook${}'.format(forgery_py.russian_tax.ogrn()))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['BREWLOCKER_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String(30))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    phone = db.Column(db.String(20))
    images = db.relationship('Image', backref='item', lazy='dynamic')

    def save_img(self, images):
        if current_app.config['S3_ENABLE']:
            for image in images:
                url = uploadToS3(image, current_app.config['S3_BUCKET'])
                db_image = Image(author=current_user._get_current_object(),
                                 item=self,
                                 url=url)
                db.session.add(db_image)
            flash("Upload successfull")
        else:
            try:
                num = self.images.count() + 1
            except:
                num = 1
            for image in images:
                new_image = images_set.save(
                    image, name='{}_{}.'.format(str(self.id), str(num)))
                url = images_set.url(new_image)
                path = images_set.path(new_image)
                db_image = Image(author=current_user._get_current_object(),
                                 item=self,
                                 path=path,
                                 url=url)
                db.session.add(db_image)
                num += 1

    def getImageList(self):
        urls = []
        for image in self.images:
            urls.append(image.url)
        return urls

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Item(header=forgery_py.lorem_ipsum.word(),
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
                     timestamp=forgery_py.date.date(True),
                     author=u,
                     phone=forgery_py.address.phone())
            db.session.add(p)
            image = Image(author=u, item=p, path='test',
                          url="http://via.placeholder.com/350x350")
            db.session.add(image)
            db.session.commit()

    def to_json(self):
        json_item = {
            'url': url_for('api.get_item', id=self.id, _external=True),
            'header': self.header,
            'body': self.body,
            'timestamp': self.timestamp,
            'images': self.getImageList()
        }
        return json_item


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    path = db.Column(db.String(), nullable=True)
    url = db.Column(db.String(), nullable=False)

    def getResponsive(self, suffix):
        # returns URL of responsive version
        directory, filename = self.url.rsplit('/', 1)
        name, ext = filename.split('.', 1)
        return "{}/responsive/{}-{}.{}".format(directory, name, suffix, ext)

    def deleteFromServer(self):
        directory, filename = self.path.rsplit('/', 1)
        name, ext = filename.split('.', 1)
        pattern = "{}/responsive/{}-*{}".format(directory, name, ext)
        try:
            for i in glob.glob(pattern):
                os.remove(i)
            os.remove(self.path)
            return
        except:
            return
