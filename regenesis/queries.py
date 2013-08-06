from sqlalchemy import func, select, and_

from regenesis.core import engine
from regenesis.database import cube_table, value_table, statistic_table
from regenesis.database import dimension_table, reference_table, get_fact_table

from pprint import pprint


def get_cube(cube_name):
    cubes = get_cubes(cube_name)
    assert len(cubes)==1, 'Multiple hits: ' + cube_name
    return cubes.pop()


def get_cubes(cube_name=None):
    ct = cube_table.table.alias('cube')
    st = statistic_table.table.alias('statistic')
    q = ct.join(st, st.c.name==ct.c.statistic_name)
    q = q.select(use_labels=True)
    if cube_name is not None:
        q = q.where(ct.c.name==cube_name)
    return list(engine.query(q))


def get_dimensions(cube_name):
    rt = reference_table.table.alias('ref')
    dt = dimension_table.table.alias('dim')
    q = rt.join(dt, rt.c.dimension_name==dt.c.name)
    q = q.select(use_labels=True)
    q = q.where(rt.c.cube_name==cube_name)
    res = engine.query(q)
    return list(res)


def query_cube(cube_name, readable=True, verbose=False):
    cube = get_cube(cube_name)
    dimensions = get_dimensions(cube_name)
    pprint(dimensions)
    
    fact_table = get_fact_table(cube_name).table.alias('fact')
    q = fact_table.select()
    selects, wheres, tables = [], [], [fact_table]
    for dim in dimensions:
        name = dim.get('dim_name')
        field = name.upper()
        title = dim.get('dim_title_de')

        if readable:
            unit = dim.get('ref_unit_name')
            if unit is not None:
                field = '%s; %s' % (field, unit)
            field = '%s (%s)' % (title, field)

        type_ = dim.get('ref_type')
        if type_ == 'measure':
            selects.append(fact_table.columns[name].label(field))
        if type_ == 'time':
            selects.append(fact_table.columns[name].label(field))
        elif type_ == 'axis':
            vt = value_table.table.alias('value_%s' % name)
            selects.append(vt.c.name.label(field + ' - ID'))
            selects.append(vt.c.title_de.label(field))
            tables.append(vt)
            wheres.append(vt.c.dimension_name==name)
            wheres.append(vt.c.value_id==fact_table.c[name])
        print [name]

    q = select(selects, and_(*wheres), tables)
    #print q
    #q = q.limit(20)
    pprint(list(engine.query(q)))


if __name__ == '__main__':
    query_cube('11111lj002')
