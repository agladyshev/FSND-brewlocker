from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

"""
For large amount of mail, should setup Celery
"""


def send_async_email(app, msg):
    # flask_mail requires application context to be active
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['BREWLOCKER_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['BREWLOCKER_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # moving request to a background thread
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
