import logging

from sqlalchemy.types import BigInteger

from regenesis.core import app, engine

log = logging.getLogger(__name__)

cube_table = engine.get_table('cube')
statistic_table = engine.get_table('statistic')
dimension_table = engine.get_table('dimension')
value_table = engine.get_table('value')
reference_table = engine.get_table('reference')


def get_fact_table(cube_name):
    return engine.get_table('fact_' + cube_name)


def load_cube(cube, update=False):
    if cube_table.find_one(name=cube.name) and not update:
        return

    engine.begin()

    cube_table.upsert(cube.to_row(), ['name'])
    statistic_table.upsert(cube.metadata.get('statistic'), ['name'])

    for dimension in cube.dimensions.values():
        dimension_table.upsert(dimension.to_row(), ['name'])
        for value in dimension.values:
            value_table.upsert(value.to_row(), ['value_id'])

    for reference in cube.references:
        reference_table.upsert(reference.to_row(), ['cube_name', 'dimension_name'])

    fact_table = get_fact_table(cube.name)
    for ref in cube.measures:
        if ref.data_type == 'GANZ':
            fact_table.create_column(ref.name, BigInteger)

    fact_table.delete()
    for i, fact in enumerate(cube.facts):
        fact_table.insert(fact.to_row())
        if i and i % 1000 == 0:
            log.info("Loaded: %s rows", i)

    engine.commit()
