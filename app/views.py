import os
from flask import render_template, redirect, session, url_for, request, g
from flask import send_from_directory
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db, lm
from forms import NewsletterForm, SearchForm, CadastroForm, LoginForm
from forms import ContatoForm, DoacaoForm
from models import Newsletter, Ong, Doacao
from hashlib import md5
from datetime import datetime
from emails import contact_email
from utils.name_utils import slug as slugfy
from flask.ext.sqlalchemy import get_debug_queries
from TwitterAPI import TwitterAPI
from config import TWITTER_API_KEY, TWITTER_API_SECRET
from config import TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from config import POST_PER_PAGE
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/<ong>/<slug>/editar', methods=['GET', 'POST'])
@login_required
def editar_doacao(ong, slug):
    user = g.user
    form = LoginForm()
    form_editar = DoacaoForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                                ong=ong.nickname))
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    if user != ong:
        abort(401)
    doacao = Doacao.query.filter_by(ong=ong, slug=slug).first_or_404()
    if form_editar.validate_on_submit():
        doacao.categoria = form_editar.categoria.data
        doacao.nome = form_editar.nome.data
        doacao.descricao = form_editar.descricao.data
        doacao.logradouro = form_editar.logradouro.data
        doacao.numero = form_editar.numero.data
        doacao.complemento = form_editar.complemento.data
        doacao.bairro = form_editar.bairro.data
        doacao.cidade = form_editar.cidade.data
        doacao.estado = form_editar.estado.data
        doacao.cep = form_editar.cep.data
        doacao.retirar = form_editar.retirar.data
        doacao.email = form_editar.email.data
        doacao.tags = form_editar.tags.data
        doacao.prioridade = form_editar.prioridade.data
        
        db.session.commit()

        return redirect(url_for('doacao', ong=ong.nickname, slug=doacao.slug))
    else:
        form_editar.categoria.data = doacao.categoria
        form_editar.nome.data = doacao.nome
        form_editar.descricao.data = doacao.descricao
        form_editar.logradouro.data = doacao.logradouro
        form_editar.numero.data = doacao.numero
        form_editar.complemento.data = doacao.complemento
        form_editar.bairro.data = doacao.bairro
        form_editar.cidade.data = doacao.cidade
        form_editar.estado.data = doacao.estado
        form_editar.cep.data = doacao.cep
        form_editar.retirar.data = doacao.retirar
        form_editar.email.data = doacao.email
        form_editar.tags.data = doacao.tags
        form_editar.prioridade.data = doacao.prioridade

        return render_template('cadastro-doacao.html',
                               form=form,
                               user=user,
                               form_cadastro=form_editar,
                               ong=ong)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(error):
    user = g.user
    form = LoginForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard', ong=ong.nickname))
    return render_template('404.html',
                           user=user,
                           form=form)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    user = g.user
    form = LoginForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard', ong=ong.nickname))
    return render_template('500.html', 
                           user=user,
                           form=form)


@app.route('/<ong>/<slug>/contato', methods=['GET', 'POST'])
def contato_doacao(ong, slug):
    user = g.user
    form = LoginForm()
    form_contato = ContatoForm()
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    doacao = Doacao.query.filter_by(ong=ong, slug=slug).first_or_404()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard', ong=ong.nickname))
    if form_contato.validate_on_submit():
        contact_email('[Pra Quem Doar] ' + doacao.nome,
                      form_contato.nome.data,
                      form_contato.email.data,
                      form_contato.mensagem.data,
                      ong.email
                      )
        return redirect(url_for('doacao', ong=ong.nickname, slug=slug))
    return render_template('contato_doacao.html', 
                           user=user,
                           form=form,
                           form_contato=form_contato,
                           doacao=doacao)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/search/<query>', methods=['GET', 'POST'])
@app.route('/search/<query>/index', methods=['GET', 'POST'])
@app.route('/search/<query>/index/<int:index>', methods=['GET', 'POST'])
def search_results(query, index=1):
    user = g.user
    form = LoginForm()
    form_busca = SearchForm()
    result_doacao = Doacao.query.filter(Doacao.tags.like('%' + query + '%')).paginate(index, POST_PER_PAGE, False)
    result_ong = Ong.query.filter(Ong.nome.like('%' + query + '%'))
    if form_busca.validate_on_submit():
        return redirect(url_for('search_results', query=form_busca.search.data))
    return render_template('search.html',
                           query=query,
                           result_doacao=result_doacao,
                           result_ong=result_ong,
                           form_busca=form_busca,
                           form=form,
                           user=user)


@app.route('/', methods=['GET', 'POST'])
def index():
    user = g.user
    form_news = NewsletterForm()
    form_busca = SearchForm()
    form = LoginForm()
    doacoes = Doacao.query.count()
    concluidas = Doacao.query.filter_by(status_id=3).count()
    tags = Doacao.query.all()
    itens = ''
    for tag in tags:
        itens += tag.tags + ','
    for categoria in tags:
        itens += categoria.categoria + ','
    tags = itens.split(',')

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
                           form=form,
                           user=user,
                           doacoes=doacoes,
                           concluidas=concluidas,
                           tags=tags)


@lm.user_loader
def load_user(id):
    return Ong.query.get(int(id))


@app.route('/<ong>/editar', methods=['GET', 'POST'])
@login_required
def editar_ong(ong):
    user = g.user
    form = LoginForm()
    form_editar = CadastroForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                                ong=ong.nickname))

    ong = Ong.query.filter_by(nickname=ong).first_or_404()

    if form_editar.validate_on_submit():
        file = request.files['logo']
        website = form_editar.website.data
        if 'http://' not in website:
            website = 'http://' + website
        
        ong.nome = form_editar.nome.data
        ong.cnpj = form_editar.cnjp.data
        ong.nickname = form_editar.nickname.data
        ong.senha = md5(form_editar.senha.data).hexdigest()
        ong.email = form_editar.email.data
        ong.descricao = form_editar.descricao.data
        ong.website = website
        ong.twitter = form_editar.twitter.data
        ong.facebook = form_editar.facebook.data
        ong.googleplus = form_editar.googleplus.data
        ong.logo = file.filename

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        db.session.commit()
        return redirect(url_for('ong_dashboard', ong=ong.nickname))
    else:
        form_editar.nome.data = ong.nome
        form_editar.cnpj.data = ong.cnpj
        form_editar.nickname.data = ong.nickname
        form_editar.email.data = ong.email
        form_editar.descricao.data = ong.descricao
        form_editar.website.data = ong.website
        form_editar.twitter.data = ong.twitter
        form_editar.facebook.data = ong.facebook
        form_editar.googleplus.data = ong.googleplus

        return render_template('cadastro.html',
                               form_cadastro=form_editar,
                               form=form,
                               user=user)


@app.route('/<ong>', methods=['GET', 'POST'])
@app.route('/<ong>/index', methods=['GET', 'POST'])
@app.route('/<ong>/index/<int:index>', methods=['GET', 'POST'])
def ong_dashboard(ong, index=1):
    user = g.user
    form = LoginForm()
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    doacoes = Doacao.query.filter_by(ong=ong).paginate(index,
                                                       POST_PER_PAGE,
                                                       False)
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
                           user=user,
                           doacoes=doacoes)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    user = g.user
    form = LoginForm()
    form_cadastro = CadastroForm()
    if form_cadastro.validate_on_submit():
        file = request.files['logo']
        website = form_cadastro.website.data
        if 'http://' not in website:
            website = 'http://' + website
        ong = Ong(nome=form_cadastro.nome.data,
                  cnpj=form_cadastro.cnpj.data,
                  nickname=form_cadastro.nickname.data,
                  senha=md5(form_cadastro.senha.data).hexdigest(),
                  email=form_cadastro.email.data,
                  descricao=form_cadastro.descricao.data,
                  website=website,
                  twitter=form_cadastro.twitter.data,
                  facebook=form_cadastro.facebook.data,
                  googleplus=form_cadastro.googleplus.data,
                  data_cadastro=datetime.now(),
                  logo=file.filename
                  )
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
        db.session.add(ong)
        db.session.commit()
        return redirect(url_for('ong_dashboard', ong=ong.nickname))
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
                           form=form,
                           user=user)


@app.route('/<ong>/<slug>', methods=['GET', 'POST'])
def doacao(ong, slug):
    user = g.user
    form = LoginForm()
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    doacao = Doacao.query.filter_by(ong=ong, slug=slug).first_or_404()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                            ong=ong.nickname))
    return render_template('doacao.html',
                            form=form,
                            user=user,
                             ong=ong,
                            doacao=doacao)


@app.route('/<ong>/doacao', methods=['GET', 'POST'])
@login_required
def cadastro_doacao(ong):
    user = g.user
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    form = LoginForm()
    form_cadastro = DoacaoForm()
    if form.validate_on_submit():
        ong = Ong.query.filter_by(nickname=form.login.data,
                                  senha=md5(form.senha_login.data).hexdigest()
                                  ).first_or_404()
        login_user(ong)
        return redirect(request.args.get('next') or
                        url_for('ong_dashboard',
                            ong=ong.nickname))
    if form_cadastro.validate_on_submit():
        doacao = Doacao(categoria=form_cadastro.categoria.data,
                        nome=form_cadastro.nome.data,
                        descricao=form_cadastro.descricao.data,
                        logradouro=form_cadastro.logradouro.data,
                        numero=form_cadastro.numero.data,
                        complemento=form_cadastro.complemento.data,
                        bairro=form_cadastro.bairro.data,
                        cidade=form_cadastro.cidade.data,
                        estado=form_cadastro.estado.data,
                        cep=form_cadastro.cep.data,
                        retirar=form_cadastro.retirar.data,
                        email=form_cadastro.email.data,
                        tags=form_cadastro.tags.data,
                        ong_id=ong.id,
                        slug=slugfy(form_cadastro.nome.data),
                        status_id=1,
                        data_cadastro=datetime.now(),
                        prioridade=form_cadastro.prioridade.data
                        )
        db.session.add(doacao)
        db.session.commit()
        api = TwitterAPI(TWITTER_API_KEY, TWITTER_API_SECRET,
                           TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
        tweet = api.request('statuses/update', {'status': '#Preciso ' + doacao.nome + ' ' + doacao.get_url() + ' #' + doacao.ong.nickname })
        return redirect(url_for('doacao', ong=ong.nickname, slug=doacao.slug))
    return render_template('cadastro-doacao.html',
                           form=form,
                           user=user,
                           form_cadastro=form_cadastro,
                           ong=ong)


@app.route('/<ong>/contato', methods=['GET', 'POST'])
def ong_contato(ong):
    user = g.user
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
    return render_template('ong_contato.html', ong=ong, form=form, form_contato=form_contato, user=user)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    user = g.user
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
    return render_template('contato.html', form=form, form_contato=form_contato, user=user)


@app.route('/ajuda')
def ajuda():
    user = g.user
    form = LoginForm()
    return render_template('ajuda.html', form=form, user=user)


@app.route('/politica')
def politica():
    user = g.user
    form = LoginForm()
    return render_template('politica.html', form=form, user=user)


@app.route('/<ong>/admin')
def instituicao_admin(ong):
    ong = Ong.query.filter_by(nickname=ong).first_or_404()
    form = LoginForm()
    return render_template('instituicao-admin.html', 
                           form=form,
                           ong=ong)


@app.after_request
def after_request(response):
    for query in get_debug_queries():
        log_msg = "DB QUERY: %s\nParams: %s\n Context: %s" % (query.statement,
                                                              query.parameters,
                                                              query.context)
        app.logger.warning(log_msg)
    return response
