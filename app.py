from datetime import datetime
from flask import Flask, render_template
from flask_script import Manager
from flask_moment import Moment

app = Flask(__name__)

manager = Manager(app)
moment = Moment(app)

@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    manager.run()
