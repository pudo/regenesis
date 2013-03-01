import logging

import sqlaload as sl

from regenesis.core import app, engine

log = logging.getLogger(__name__)




def load_cube(cube):
    cube_table = sl.get_table(engine, 'cube')
    sl.upsert(engine, cube_table, cube.to_row(), ['name'])

    statistic_table = sl.get_table(engine, 'statistic')
    sl.upsert(engine, statistic_table, cube.metadata.get('statistic'), ['name'])

    dimension_table = sl.get_table(engine, 'dimension')
    value_table = sl.get_table(engine, 'value')
    for dimension in cube.dimensions.values():
        sl.upsert(engine, dimension_table,
                  dimension.to_row(), ['name'])
        for value in dimension.values:
            sl.upsert(engine, value_table,
                      value.to_row(), ['value_id'])

    reference_table = sl.get_table(engine, 'reference')
    for reference in cube.references:
        sl.upsert(engine, reference_table,
                  reference.to_row(), ['cube_name', 'dimension_name'])

    fact_table = sl.get_table(engine, 'fact_' + cube.name)
    for fact in cube.facts:
        sl.upsert(engine, fact_table,
                  fact.to_row(), ['fact_id'])

