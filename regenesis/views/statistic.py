from flask import Blueprint, render_template

from regenesis.core import app, engine, get_catalog
from regenesis.database import statistic_table

blueprint = Blueprint('statistic', __name__)


@blueprint.route('/<catalog>/statistics')
def index(catalog):
    catalog = get_catalog(catalog)
    statistics = statistic_table.find(order_by='title_de')
    return render_template('statistic/index.html',
                           catalog=catalog,
                           statistics=statistics)


@blueprint.route('/<catalog>/statistics/<name>')
def view(catalog, name):
    catalog = get_catalog(catalog)
    statistic = statistic_table.find_one(name=name)
    return render_template('statistic/view.html',
                           catalog=catalog,
                           statistic=statistic)
