from flask import render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db, lm
from forms import NewsletterForm
from models import Newsletter


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewsletterForm()
    if form.validate_on_submit():
        news = Newsletter(nome=form.nome.data,
                          email=form.email.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form)


@lm.user_loader
def load_user(id):
    return Ong.query.get(int(id))


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')
