import logging
from logging.handlers import RotatingFileHandler
import time

# third-party imports
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask.json import JSONEncoder


db = SQLAlchemy()
login_manager = LoginManager()
# Limit request rate per route. Gives client HTTP 429 when exceeded.
limiter = Limiter(key_func=get_remote_address,
                  default_limits=["200 per day", "50 per hour"])


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('flaskv.default_settings')
    app.config.from_envvar('FLASKV_SETTINGS')

    logpath = app.config.get('LOG_FILEPATH')
    handler = RotatingFileHandler(logpath, maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    limiter.init_app(app)

    bootstrap = Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "home.login"

    migrate = Migrate(app, db)

    from . import models

    from . import auth
    app.register_blueprint(auth.bp)
    from . import room
    app.register_blueprint(room.bp)

    login_manager.blueprint_login_views = {
        'auth': '/login',
        'admin': '/login',
        'room': '/login',
    }

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/homepage')
    def homepage():
        return 'Homepage'

    return app
