from pprint import pprint 

from regenesis.core import app, engine
from regenesis.database import statistic_table, cube_table, reference_table
from regenesis.queries import get_cubes, get_dimensions

def find_denormalized():
    res = {}
    for cube in get_cubes():
        statistic = cube.get('statistic_name')
        if not statistic in res:
            res[statistic] = {}
        cube_name = cube.get('cube_name')
        dimensions = get_dimensions(cube_name)
        #pprint(dimensions)
        dimensions = [d for d in dimensions if not d['dim_measure_type'].startswith('K-REG-MM')]
        #dims = [(d['dim_name'], d['ref_type']) for d in dimensions]
        dims = [d['dim_name'] for d in dimensions]
        res[statistic][cube_name] = dims
    pprint(res)
