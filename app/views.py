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


@app.before_request
def before_request():
    g.user = current_user


@app.route('/search/<query>', methods=['GET', 'POST'])
def search_results(query):
    form = LoginForm()
    form_search = SearchForm()
    result_doacao = Doacao.query.filter(Doacao.tags.like('%' + query + '%'))
    result_ong = Ong.query.filter(Ong.nome.like('%' + query + '%'))
    if form_search.validate_on_submit():
        return redirect(url_for('search_results', query=form_search.search.data))
    return render_template('search.html',
                           query=query,
                           results=results,
                           form_search=form_search,
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
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard', ong=ong.nickname))
    return render_template('index.html',
                           form_news=form_news,
                           form_busca=form_busca,
                           form=form)


@lm.user_loader
def load_user(id):
    return Ong.query.get(int(id))


@app.route('/<ong>', methods=['GET', 'POST'])
def ong_dashboard(ong):
    user = g.user
    form = LoginForm()
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                            ong=ong.nickname))
    return render_template('instituicao.html',
                           ong=ong,
                           form=form,
                           user=user)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = LoginForm()
    form_cadastro = CadastroForm()
    if form_cadastro.validate_on_submit():
        ong = Ong(nome=form_cadastro.nome.data,
                  cnpj=form_cadastro.cnpj.data,
                  nickname=form_cadastro.nickname.data,
                  senha=md5(form_cadastro.senha.data).hexdigest(),
                  email=form_cadastro.email.data,
                  descricao=form_cadastro.descricao.data,
                  website=form_cadastro.website.data,
                  twitter=form_cadastro.twitter.data,
                  facebook=form_cadastro.facebook.data,
                  googleplus=form_cadastro.googleplus.data,
                  data_cadastro=datetime.now()
                  )
        db.session.add(ong)
        db.session.commit()
        return redirect(url_for('org_dashboard', ong=ong.nickname))
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                            ong=ong.nickname))

    return render_template('cadastro.html',
                           form_cadastro=form_cadastro,
                           form=form)


@app.route('/doacao')
def doacao():
    return render_template('doacao.html')


@app.route('/<ong>/doacao')
def cadastro_doacao(ong):
    user = g.user
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    form = LoginForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                            ong=ong.nickname))

    return render_template('cadastro-doacao.html',
                           form=form,
                           user=user,
                           ong=ong)


@app.route('/<ong>/contato', methods=['GET', 'POST'])
def ong_contato(ong):
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    form = LoginForm()
    form_contato = ContatoForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                            ong=ong.nickname))

    if form_contato.validate_on_submit():
        contact_email('[Pra Quem Doar Contato] ' + form_contato.assunto.data,
                      form_contato.nome.data,
                      form_contato.email.data,
                      form_contato.mensagem.data,
                      ong.email
                      )
        return redirect(url_for('ong_contato', ong=ong.nickname))
    return render_template('ong_contato.html', ong=ong, form=form, form_contato=form_contato)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    form = LoginForm()
    form_contato = ContatoForm()
    if form_contato.validate_on_submit():
        contact_email('[Pra Quem Doar Contato] ' + form_contato.assunto.data,
                      form_contato.nome.data,
                      form_contato.email.data,
                      form_contato.mensagem.data,
                      'contato@aleborba.com.br'
                      )
        return redirect(url_for('contato'))
    return render_template('contato.html', form=form, form_contato=form_contato)


@app.route('/busca')
def busca():
    form = LoginForm()
    return render_template('busca.html', form=form)


@app.route('/single')
def single():
    form = LoginForm()
    return render_template('single.html', form=form)


@app.route('/<ong>/admin')
def instituicao_admin(ong):
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    form = LoginForm()
    return render_template('instituicao-admin.html', 
                           form=form,
                           ong=ong)


@app.route('/404')
def erro_404():
    form = LoginForm()
    return render_template('404.html', 
                           form=form)
    
    
@app.route('/500')
def erro_500():
    form = LoginForm()
    return render_template('500.html', 
                           form=form)
    
    
