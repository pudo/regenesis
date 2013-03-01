import json
import logging
from flask.ext.script import Manager

from regenesis.core import app
from regenesis.export import JSONEncoder
from regenesis.retrieve import fetch_index, fetch_cube
from regenesis.database import load_cube

manager = Manager(app)
log = logging.getLogger(__name__)

from pprint import pprint


def dump_json(cube):
    fh = open('exports/%s.json' % cube.name, 'wb')
    json.dump(cube, fh, cls=JSONEncoder, indent=2)
    fh.close()


def get_catalog(catalog_name):
    catalog = app.config.get('CATALOG').get(catalog_name)
    if catalog is None:
        raise ValueError('No such catalog: %s' % catalog_name)
    return catalog


@manager.command
def harvestcube(catalog_name, cube_name):
    """ Dump a single cube from a catalog. """
    catalog = get_catalog(catalog_name)
    cube = fetch_cube(catalog, cube_name)
    dump_json(cube)
    load_cube(cube)


@manager.command 
def harvest(catalog_name):
    """ Dump all cubes from a catalog. """
    catalog = get_catalog(catalog_name)
    for cube_name in fetch_index(catalog):
        log.info("Loading: %s", cube_name)
        cube = fetch_cube(catalog, cube_name)
        dump_json(cube)
        load_cube(cube)

#    #cube = fetch_cube('12613BJ003')
#    cube = fetch_cube('52411KJ001')

if __name__ == '__main__':
    manager.run()

