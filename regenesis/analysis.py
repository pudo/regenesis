from pprint import pprint 

from regenesis.core import app, engine
from regenesis.database import statistic_table, cube_table, reference_table

import sqlaload as sl

def find_denormalized():
    statistics = list(sl.find(engine, statistic_table))
    for statistic in statistics:
        cuboids = {}
        cubes = list(sl.find(engine, cube_table,
            statistic_name=statistic.get('name')))
        for cube in cubes:
            refs = list(sl.find(engine, reference_table,
                cube_name=cube.get('name')))
            cuboids[cube.get('name')] = \
                [r.get('dimension_name') for r in refs]
        pprint(cuboids)



