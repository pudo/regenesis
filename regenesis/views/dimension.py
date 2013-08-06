from flask import Blueprint, render_template
from sqlalchemy import func, select, and_

from regenesis.core import app, engine, get_catalog
from regenesis.database import dimension_table, value_table
from regenesis.database import cube_table, statistic_table, reference_table

blueprint = Blueprint('dimension', __name__)

def get_statistics(dimension_name=None):
    ct = cube_table.table.alias('cube')
    st = statistic_table.table.alias('statistic')
    rt = reference_table.table.alias('reference')
    tables = [ct, st, rt]
    wheres = [
      st.c.name==ct.c.statistic_name,
      rt.c.cube_name==ct.c.name,
      rt.c.dimension_name==dimension_name
      ]
    q = select([st], and_(*wheres), tables, distinct=True)
    return list(engine.query(q))

@blueprint.route('/<catalog>/dimensions/<name>.html')
def view(catalog, name):
    catalog = get_catalog(catalog)
    dimension = dimension_table.find_one(name=name)
    values = list(value_table.find(dimension_name=name, order_by='title_de'))
    has_values = len(values) > 0
    statistics = get_statistics(name)
    return render_template('dimension/view.html',
                           catalog=catalog,
                           statistics=statistics,
                           values=values,
                           has_values=has_values,
                           dimension=dimension)
