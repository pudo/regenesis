from flask import Blueprint, render_template

from regenesis.core import app, engine, get_catalog
from regenesis.database import dimension_table, value_table

blueprint = Blueprint('dimension', __name__)


@blueprint.route('/<catalog>/dimensions/<name>')
def view(catalog, name):
    catalog = get_catalog(catalog)
    dimension = dimension_table.find_one(name=name)
    values = value_table.find(dimension_name=name, order_by='title_de')
    return render_template('dimension/view.html',
                           catalog=catalog,
                           values=values,
                           dimension=dimension)
