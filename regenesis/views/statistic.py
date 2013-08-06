from flask import Blueprint, render_template
from collections import defaultdict

from regenesis.core import app, engine, get_catalog
from regenesis.views.util import dimension_type_text
from regenesis.database import statistic_table, cube_table
from regenesis.queries import get_dimensions
from regenesis.views.util import parse_description

blueprint = Blueprint('statistic', __name__)

ADM_RANKS = {
    'gemein': 1,
    'kreise': 2,
    'regbez': 3,
    'dland': 4,
    'dinsg': 5
}

def get_cubes(statistic_name=None):
    q = cube_table.table.select()
    q = q.where(cube_table.table.c.statistic_name==statistic_name)
    return list(engine.query(q))

@blueprint.route('/<catalog>/statistics/<name>.html')
def view(catalog, name):
    catalog = get_catalog(catalog)
    statistic = statistic_table.find_one(name=name)
    desc = parse_description(statistic['description_de'])
    cubes = []
    dims = defaultdict(int)
    for cube in get_cubes(name):
      cube['dimensions'] = get_dimensions(cube['name'])
      for dim in cube['dimensions']:
        dim['show'] = True
        dims[dim['dim_name']] += 1
        dim['type_text'] = dimension_type_text(dim['dim_measure_type'])
        if dim['dim_measure_type'].startswith('K-REG'):
            cube['admlevel'] = (ADM_RANKS[dim['dim_name']], dim['dim_title_de'], dim['dim_name'])
            dim['show'] = False
      cube['stand'] = cube['provenance'].split('hat am')[-1].split('um')[0].strip()
      cubes.append(cube)
    common = [d for d, i in dims.items() if i == len(cubes)]
    commons = {}
    for cube in cubes:
        for dim in cube['dimensions']:
            if dim['dim_name'] in common and dim['show']:
                #dim['show'] = False
                commons[dim['dim_name']] = dim
    return render_template('statistic/view.html',
                           catalog=catalog,
                           desc=desc,
                           cubes=cubes,
                           common=commons.values(),
                           has_common=len(common) > 0,
                           statistic=statistic)
