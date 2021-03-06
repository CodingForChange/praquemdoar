from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, IntegerField
from wtforms import TextAreaField, SelectField
from wtforms.validators import Required, Length
from app.models import Ong


class ContatoForm(Form):
    nome = TextField('nome', validators=[Required(), Length(max=120)])
    email = TextField('email', validators=[Required(), Length(max=120)])
    assunto = TextField('assunto', validators=[Length(max=120)])
    mensagem = TextAreaField('mensagem', validators=[Required()])


class NewsletterForm(Form):
    nome = TextField('nome', validators=[Required(), Length(max=120)])
    email = TextField('email', validators=[Required(), Length(max=120)])


class CadastroForm(Form):
    nome = TextField('nome', validators=[Required(), Length(max=120)])
    email = TextField('email', validators=[Required(), Length(max=120)])
    cnpj = TextField('cnpj', validators=[Required()])
    nickname = TextField('nickname', validators=[Required()])
    senha = TextField('senha', validators=[Required(), Length(max=200)])
    logo = TextField('logo')
    descricao = TextAreaField('descricao', validators=[Length(max=200)])
    website = TextField('website')
    twitter = TextField('twitter')
    facebook = TextField('facebook')
    googleplus = TextField('googleplus')


class DoacaoForm(Form):
    nome = TextField('nome', validators=[Required(), Length(max=120)])
    descricao = TextField('descricao', validators=[Length(max=200)])
    logradouro = TextField('logradouro', validators=[Required(),
                                                     Length(max=200)])
    numero = TextField('numero', validators=[Required(), Length(max=20)])
    complemento = TextField('complemento')
    bairro = TextField('bairro', validators=[Required(), Length(max=120)])
    cidade = TextField('cidade', validators=[Required(), Length(max=120)])
    estado = TextField('estado', validators=[Required(), Length(max=2)])
    cep = TextField('cep', validators=[Required()])
    retirar = BooleanField('retirar', validators=[Required()])
    email = TextField('email')
    tags = TextField('tags', validators=[Required()])
    categoria = SelectField('categoria', choices=[('Roupas', 'Roupas'),
                                                   ('Dinheiro', 'Dinheiro'),
                                                   ('Moveis', 'Moveis'),
                                                   ('Eletronicos', 'Eletronicos'),
                                                   ('Brinquedos','Brinquedos'),
                                                   ('Alimentos', 'Alimentos'),
                                                   ('Higiene', 'Higiene')],
                                         validators=[Required()])
    publicar = BooleanField('publicar')
    prioridade = SelectField('prioridade', choices=[('Alta Prioridade', 'Alta Prioridade'),
                                                    ('Baixa Prioridade', 'Baixa Prioridade')],
                                           validators=[Required()])


class SearchForm(Form):
    search = TextField('search', validators=[Required()])


class LoginForm(Form):
    login = TextField('login', validators=[Required()])
    senha_login = TextField('senha_login', validators=[Required()])
