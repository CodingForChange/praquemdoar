from flask import render_template, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user
from flask.ext.login import current_user, login_required
from app import app, db


@app.route('/')
def index():
    return render_template('index.html')


@lm.user_loader
def load_user(id):
    return Ong.query.get(int(id))


@app.route('/cadastro')
def cadastro():
    return None
