from flask import render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db, lm
from forms import NewsletterForm, SearchForm, CadastroForm
from models import Newsletter, Ong
from hashlib import md5
from datetime import datetime


@app.route('/search/<query>', methods=['GET', 'POST'])
def search_results(query):
    form = SearchForm()
    result_doacao = Doacao.query.filter(Doacao.tags.like('%' + query + '%'))
    result_ong = Ong.query.filter(Ong.nome.like('%' + query + '%'))
    if form.validate_on_submit():
        return redirect(url_for('search_results', query=form.search.data))
    return render_template('search.html',
                           query=query,
                           results=results,
                           form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NewsletterForm()
    form_busca = SearchForm()
    if form.validate_on_submit():
        news = Newsletter(nome=form.nome.data,
                          email=form.email.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    if form_busca.validate_on_submit():
        return redirect(url_for('search_results', query=form.search.data))
    return render_template('index.html', form=form, form_busca=form_busca)


@lm.user_loader
def load_user(id):
    return Ong.query.get(int(id))


@app.route('/<ong>')
def org_dashboard(ong):
    return None


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if form.validate_on_submit():
        ong = Ong(nome=form.nome.data,
                  cnpj=form.cnpj.data,
                  nickname=form.nickname.data,
                  senha=md5(form.senha.data).hexdigest(),
                  email=form.email.data,
                  descricao=form.descricao.data,
                  website=form.website.data,
                  twitter=form.twitter.data,
                  facebook=form.facebook.data,
                  googleplus=form.googleplus.data,
                  data_cadastro=datetime.now()
                  )
        db.session.add(ong)
        db.session.commit()
        return redirect(url_for('org_dashboard', ong=ong.nickname))
    return render_template('cadastro.html', form=form)


@app.route('/instituicao')
def instituicao():
    return render_template('instituicao.html')
    

@app.route('/doacao')
def doacao():
    return render_template('doacao.html')
