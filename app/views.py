from . import app
from flask import render_template, request, redirect, url_for

@app.route('/')
def home():
    return render_template('resume.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')