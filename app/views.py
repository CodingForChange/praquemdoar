from flask import render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db, lm
from forms import NewsletterForm, SearchForm, CadastroForm, LoginForm
from forms import ContatoForm
from models import Newsletter, Ong
from hashlib import md5
from datetime import datetime
from emails import contact_email


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
    form_news = NewsletterForm()
    form_busca = SearchForm()
    form = LoginForm()
    if form_news.validate_on_submit():
        news = Newsletter(nome=form_news.nome.data,
                          email=form_news.email.data)
        db.session.add(news)
        db.session.commit()
        return redirect(url_for('index'))
    if form_busca.validate_on_submit():
        return redirect(url_for('search_results', query=form_busca.search.data))
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexadigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or url_for('ong_dashboard'))
    return render_template('index.html',
                           form_news=form_news,
                           form_busca=form_busca,
                           form=form)


@lm.user_loader
def load_user(id):
    return Ong.query.get(int(id))


@app.route('/<ong>', methods=['GET', 'POST'])
def org_dashboard(ong):
    form = LoginForm()
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    return render_template('instituicao.html', ong=ong, form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = LoginForm()
    form_cadastro = CadastroForm()
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
    return render_template('cadastro.html',
                           form_cadastro=form_cadastro,
                           form=form)


@app.route('/doacao')
def doacao():
    return render_template('doacao.html')


@app.route('/instituicao-contato')
def instituicao_contato():
    return render_template('instituicao-contato.html')


@app.route('/cadastro-doacao')
def cadastro_doacao():
    return render_template('cadastro-doacao.html')


@app.route('/<ong>/contato', methods=['GET', 'POST'])
def ong_contato(ong):
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    form = ContatoForm()
    if form.validate_on_submit():
        contact_email('[Pra Quem Doar Contato] ' + form.assunto.data,
                      form.nome.data,
                      form.email.data,
                      form.mensagem.data,
                      ong.email
                      )
        return redirect(url_for('ong_contato', ong=ong.nickname))
    return render_template('ong_contato.html', ong=ong, form=form)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    if form.validate_on_submit():
        contact_email('[Pra Quem Doar Contato] ' + form.assunto.data,
                      form.nome.data,
                      form.email.data,
                      form.mensagem.data,
                      'contato@aleborba.com.br'
                      )
        return redirect(url_for('contato'))
    return render_template('contato.html', form=form)
