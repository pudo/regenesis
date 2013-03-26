from flask import render_template, Response, request
from flask import session, redirect, flash, Markup

from regenesis.core import app

@app.route('/')
def index():
    return render_template('index.html')



