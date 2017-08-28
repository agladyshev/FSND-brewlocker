from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from oauth import OAuthSignIn
from . import auth
from .. import db
from ..models import User


@auth.route('/login')
def login():
	return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@auth.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    oauth = OAuthSignIn.get_provider(provider)
    provider_id, username = oauth.callback()
    if provider_id is None:
        flash('Authentication failed.')
        return redirect(url_for('main.index'))
    user = User.query.filter_by(provider_id=provider_id).first()
    if not user:
        user = User(provider_id=provider_id, username=username)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('main.index'))