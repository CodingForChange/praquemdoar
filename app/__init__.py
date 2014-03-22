import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir, ADMINS


app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/ttr.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:' +
                                                ' %(message)s [in ' +
                                                '%(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Ticket to ride Startup')


from app import views, models
