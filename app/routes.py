from app import app
from flask import render_template,flash,redirect, request, url_for

@app.route('/')
@app.route('/index')
def index():
    return 'hello'
