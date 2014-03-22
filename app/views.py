from flask import render_template, redirect, session, url_for, request, g
from app import app, db

@app.route('/')
def index():
    return render_template('index.html')
