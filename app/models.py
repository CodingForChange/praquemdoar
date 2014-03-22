from hashlib import md5
from datetime import datetime
from app import db


doacoes = db.Table('doacoes',
                   db.Column('ong_id', db.Integer,
                             db.ForeignKey('ong.id')),
                   db.Column('doacao_id', db.Integer,
                             db.ForeignKey('doacao.id'))
                   )

class Ong(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(20), index=True, unique=True)
    nome = db.Column(db.String(120))
    cnpj = db.Column(db.Integer, index=True, unique=True)
    senha = db.Column(db.String(255))
    email = db.Column(db.String(120))
    logo = db.Column(db.String(120))
    descricao = db.Column(db.String(200))
    website = db.Column(db.String(120))
    twitter = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    googleplus = db.Column(db.String(120))
    data_cadastro = db.Column(db.DateTime)
    doacoes = db.relationship('Doacao',
                              secondary=doacoes,
                              backref=db.backref('ongs',
                                                 lazy='dynamic'),
                              lazy='dynamic'
                              )

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)

    def __repr__(self):  # pragma: no cover
        return '<Ong %r>' % (self.nome)


class Doacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), index=True)
    descricao = db.Column(db.String(200))
    logradouro = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(30))
    cidade = db.Column(db.String(50))
    estado = db.Column(db.String(2))
    cep = db.Column(db.Integer)
    retirar = db.Column(db.Boolean)
    email = db.Column(db.String(120))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))
    data_cadastro = db.Column(db.DateTime)
    tags = db.Column(db.String(200))

    def __repr__(self):  # pragma: no cover
        return '<Doacao %r>' % (self.nome)


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    doacoes = db.relationship('Doacao', backref='status', lazy='dynamic')

    def __repr__(self):  # pragma: no cover
        return '<Status %r>' % (self.nome)
