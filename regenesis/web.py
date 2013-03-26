from flask import render_template, Response, request
from flask import session, redirect, flash, Markup

from regenesis.core import app
from regenesis.views.dimension import blueprint as dimension_blueprint
from regenesis.views.statistic import blueprint as statistic_blueprint

app.register_blueprint(dimension_blueprint)
app.register_blueprint(statistic_blueprint)

@app.template_filter('text')
def text_filter(s):
    if s is None:
        return ''
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.replace('\n', '<br>\n')
    #from markdown import markdown
    #s = markdown(s)
    #s = s.replace('h3>', 'h4>')
    #s = s.replace('h2>', 'h3>')
    #s = s.replace('h1>', 'h2>')
    return Markup(s)

@app.route('/')
def index():
    return render_template('index.html')



