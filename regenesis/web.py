#coding: utf-8
from flask import render_template, Response, request
from flask import session, redirect, flash, Markup, url_for

from regenesis.core import app
from regenesis.views.util import dimension_type_text as _dimension_type_text
from regenesis.views.dimension import blueprint as dimension_blueprint
from regenesis.views.statistic import blueprint as statistic_blueprint
from regenesis.views.catalog import blueprint as catalog_blueprint

app.register_blueprint(dimension_blueprint)
app.register_blueprint(statistic_blueprint)
app.register_blueprint(catalog_blueprint)

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

@app.template_filter('wraptext')
def text_filter_wrapped(s):
    if s is None:
        return ''
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.replace('\n \n', '</p><p>\n')
    #from markdown import markdown
    #s = markdown(s)
    #s = s.replace('h3>', 'h4>')
    #s = s.replace('h2>', 'h3>')
    #s = s.replace('h1>', 'h2>')
    return Markup('<p>' + s + '</p>')


@app.template_filter()
def dimension_type_text(type_name):
    return _dimension_type_text(type_name)


@app.route('/favicon.ico')
def nop():
    return Response(status=404)

@app.route('/index.html')
def index():
    name, catalog = app.config.get('CATALOG').items().pop()
    return redirect(url_for('catalog.view', catalog=name))



