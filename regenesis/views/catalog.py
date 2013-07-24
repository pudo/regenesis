from flask import Blueprint, render_template

from regenesis.core import app, engine, get_catalog
from regenesis.database import statistic_table

blueprint = Blueprint('catalog', __name__)


@blueprint.route('/<catalog>')
def view(catalog):
    catalog = get_catalog(catalog)
    return render_template('catalog/index.html',
                           catalog=catalog)
