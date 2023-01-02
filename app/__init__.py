from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, ender_as_batch=True)

# Set up logging to file.
if not app.debug:
    if not os.path.exists('logs/'):
        os.mkdir('logs/')

    # Only store 1M of data in the logs.
    file_handler = RotatingFileHandler('logs/wedding-website.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    # Write line to log each time the app is launched.
    app.logger.setLevel(logging.INFO)
    app.logger.info('Wedding App startup')

from app import routes, models