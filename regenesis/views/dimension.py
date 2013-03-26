from flask import Blueprint, render_template

import sqlaload as sl
from regenesis.core import app, engine

dimension_table = sl.get_table(engine, 'dimension')
value_table = sl.get_table(engine, 'value')

blueprint = Blueprint('dimension', __name__)

@blueprint.route('/<catalog>/dimensions')
def index(catalog):
    dimensions = sl.find(engine, dimension_table,
            order_by='title_de')
    return render_template('dimension/index.html',
            catalog=catalog,
            dimensions=dimensions)

@blueprint.route('/<catalog>/dimensions/<name>')
def view(catalog, name):
    dimension = sl.find_one(engine, dimension_table, name=name)
    values = sl.find(engine, value_table, dimension_name=name, 
                order_by='title_de')
    return render_template('dimension/view.html',
            catalog=catalog,
            values=values,
            dimension=dimension)



