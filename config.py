import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'aeljawoeiruaoesjfasodj6.498462168#$@#EWREOkoKo'

SENDGRID_USER = 'ale_borba'
SENDGRID_PASS = 't1ck3t'

ADMINS = ['ale@sample.com']
