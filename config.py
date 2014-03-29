import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'aeljawoeiruaoesjfasodj6.498462168#$@#EWREOkoKo'

SENDGRID_USER = 'ale_borba'
SENDGRID_PASS = 't1ck3t'

ADMINS = ['ale@sample.com']

TWITTER_API_KEY = '5TZC61CJmPfF1yELWI2eJw'
TWITTER_API_SECRET = '1zaYaiQLEnmuAaZrDicoNESyShYCPpym3V8VUeDwxo'
TWITTER_ACCESS_TOKEN = '2403586152-UuLQCv6srAcMqk3iB3zsttbzVcL7KFbg285s9Ef'
TWITTER_ACCESS_SECRET = 'Y8H9z6CbUIrVsYHdshXFcJAdOVLzvyqf2HaeRHy73l6Hl'

UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

POST_PER_PAGE = 5
