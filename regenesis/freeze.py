import os
import shutil
from dataset import freeze

from regenesis.queries import get_all_statistics, get_all_dimensions
from regenesis.queries import get_cubes, query_cube
from regenesis.database import value_table
from regenesis.util import slugify
from regenesis.web import app
from regenesis.core import engine

client = app.test_client()

def get_output_dir():
    return os.path.join( app.root_path, '..', 'build')
    #return '/Users/fl/tmp/regenesis'

def freeze_request(req_path):
    print "Freezing %s..." % req_path
    path = os.path.join(get_output_dir(), req_path.lstrip('/'))
    dirname = os.path.dirname(path)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    fh = open(path, 'w')
    res = client.get(req_path)
    fh.write(res.data)
    fh.close()


def freeze_html():
    print "Copying /static..."
    outdir = os.path.join(get_output_dir(), 'static')
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    shutil.copytree(app.static_folder, outdir)
    freeze_request('/index.html')
    freeze_request('/faq.html')
    freeze_request('/api.html')
    freeze_request('/contact.html')
    for catalog in ['regional']:
        freeze_request('/%s/index.html' % catalog)
        for dimension in get_all_dimensions():
            freeze_request('/%s/dimensions/%s.html' % (catalog, dimension['name']))
        for statistic in get_all_statistics():
            slug = slugify(statistic['title_de'])
            freeze_request('/%s/statistics/%s.%s.html' % (catalog, slug, statistic['name']))


def freeze_data():
    print "Freezing dimension values..."
    prefix = os.path.join(get_output_dir(), 'data', 'dimensions')
    freeze(value_table.all(), prefix=prefix, filename='{{dimension_name}}.csv', format='csv')
    freeze(value_table.all(), prefix=prefix, filename='{{dimension_name}}.json', format='json')

    print "Freezing cubes..."
    for cube in get_cubes():
        prefix = os.path.join(get_output_dir(), 'data',
                              cube['statistic_name'],
                              cube['cube_name'])
        slug = slugify(cube['statistic_title_de'])
        for (text, rb) in [('labeled', True), ('raw', False)]:
            q, ps = query_cube(cube['cube_name'], readable=rb)
            fn = '%s-%s-%s.csv' % (slug, cube['cube_name'], text)
            print [fn]
            freeze(engine.query(q), prefix=prefix, filename=fn)
            #print cube['cube_name']

if __name__ == '__main__':
    freeze_data()
    freeze_html()

