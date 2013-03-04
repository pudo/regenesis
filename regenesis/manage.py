import logging
from flask.ext.script import Manager

from regenesis.core import app
from regenesis.export import JSONEncoder
from regenesis.storage import store_cube_raw, load_cube_raw, \
    dump_cube_json
from regenesis.retrieve import fetch_index, fetch_cube
from regenesis.database import load_cube

manager = Manager(app)
log = logging.getLogger(__name__)

from pprint import pprint

def get_catalog(catalog_name):
    catalog = app.config.get('CATALOG').get(catalog_name)
    if catalog is None:
        raise ValueError('No such catalog: %s' % catalog_name)
    return catalog


@manager.command
def fetchcube(catalog_name, cube_name):
    """ Dump a single cube from a catalog. """
    catalog = get_catalog(catalog_name)
    cube_data = fetch_cube(catalog, cube_name)
    store_cube_raw(cube_name, cube_data)


@manager.command 
def fetch(catalog_name):
    """ Dump all cubes from a catalog. """
    catalog = get_catalog(catalog_name)
    for cube_name in fetch_index(catalog):
        log.info("Fetching: %s", cube_name)
        cube_data = fetch_cube(catalog, cube_name)
        store_cube_raw(cube_name, cube_data)


@manager.command
def loadcube(catalog_name, cube_name):
    """ Load a single cube into a database. """
    load_cube_raw(cube_name)
    load_cube(cube)


@manager.command 
def load(catalog_name):
    """ Load all cubes into a database. """
    catalog = get_catalog(catalog_name)
    for cube_name in fetch_index(catalog):
        log.info("Loading: %s", cube_name)
        load_cube_raw(cube_name)
        load_cube(cube)

#    #cube = fetch_cube('12613BJ003')
#    cube = fetch_cube('52411KJ001')

if __name__ == '__main__':
    manager.run()

