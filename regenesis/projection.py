from regenesis.queries import get_cubes, query_cube
from regenesis.core import engine
from regenesis.util import slugify

def make_views():
    for cube in get_cubes():
        slug = slugify(cube.get('statistic_title_de'))
        slug = slug.replace('-', '_')
        slug = slug + '_' + cube.get('cube_name')
        q = 'DROP VIEW IF EXISTS ' + slug
        engine.query(q)
        q, params = query_cube(cube.get('cube_name'), readable=False)
        q = 'CREATE VIEW ' + slug + ' AS ' + unicode(q)
        engine.query(q, **params)
        print [slug, q]

if __name__ == '__main__':
    make_views()
