from flask import Blueprint, render_template

from regenesis.core import app, engine, get_catalog
from regenesis.database import statistic_table

blueprint = Blueprint('statistic', __name__)


@blueprint.route('/<catalog>/statistics/<name>')
def view(catalog, name):
    catalog = get_catalog(catalog)
    statistic = statistic_table.find_one(name=name)
    return render_template('statistic/view.html',
                           catalog=catalog,
                           statistic=statistic)
