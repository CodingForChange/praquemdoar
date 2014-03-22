from flask.ext.wtf import Form
from wtforms import TextField, BooleanField
from wtforms.validators import Required, Length
from app.models import Ong


class NewsletterForm(Form):
    nome = TextField('nome', validators=[Required(), Length(max=120)])
    email = TextField('email', validators=[Required(), Length(max=120)])
