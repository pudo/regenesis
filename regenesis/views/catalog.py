from flask import Blueprint, render_template

from regenesis.core import app, engine, get_catalog
from regenesis.views.util import dimension_type_text
from regenesis.database import statistic_table, dimension_table

blueprint = Blueprint('catalog', __name__)


@blueprint.route('/<catalog>/index.html')
def view(catalog):
    catalog = get_catalog(catalog)
    statistics = statistic_table.find(order_by='title_de')
    dimensions = []
    for dimension in dimension_table.find(order_by='title_de'):
        dimension['measure_type_name'] = dimension_type_text(dimension['measure_type'])
        dimensions.append(dimension)

    return render_template('catalog/index.html',
                           catalog=catalog,
                           statistics=statistics,
                           dimensions=dimensions)
