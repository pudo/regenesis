import logging
from flask.ext.script import Manager

from regenesis.core import app, get_catalog
from regenesis.export import JSONEncoder
from regenesis.cube import Cube
from regenesis.web import app
from regenesis.storage import store_cube_raw, load_cube_raw, \
    dump_cube_json, exists_raw
from regenesis.retrieve import fetch_index, fetch_cube
from regenesis.database import load_cube

manager = Manager(app)
log = logging.getLogger(__name__)


@manager.command
def fetchcube(catalog_name, cube_name):
    """ Dump a single cube from a catalog. """
    catalog = get_catalog(catalog_name)
    cube_data = fetch_cube(catalog, cube_name)
    if cube_data is None:
        log.warn("Could not fetch: %s", cube_name)
    else:
        store_cube_raw(catalog_name, cube_name, cube_data)


@manager.command
def fetch(catalog_name, update=False):
    """ Dump all cubes from a catalog. """
    catalog = get_catalog(catalog_name)
    for cube_name in fetch_index(catalog):
        if not exists_raw(catalog_name, cube_name) or update:
            log.info("Fetching: %s", cube_name)
            try:
                cube_data = fetch_cube(catalog, cube_name)
                if cube_data is None:
                    log.warn("Could not fetch: %s", cube_name)
                else:
                    store_cube_raw(catalog_name, cube_name, cube_data)
            except Exception, e:
                log.exception(e)


@manager.command
def loadcube(catalog_name, cube_name):
    """ Load a single cube into a database. """
    cube_data = load_cube_raw(catalog_name, cube_name)
    cube = Cube(cube_name, cube_data)
    log.info("Loading: %s (%s facts)", cube_name, len(cube.facts))
    load_cube(cube)


@manager.command
def load(catalog_name, update=False):
    """ Load all cubes into a database. """
    catalog = get_catalog(catalog_name)
    for cube_name in fetch_index(catalog):
        if exists_raw(catalog_name, cube_name):
            cube_data = load_cube_raw(catalog_name, cube_name)
            cube = Cube(cube_name, cube_data)
            log.info("Loading: %s (%s facts)", cube_name, len(cube.facts))
            load_cube(cube, update=update)


@manager.command
def freezedata():
    """ Generate flat files for data. """
    from regenesis.freeze import freeze_data
    freeze_data()


@manager.command
def freezehtml():
    """ Generate flat files for HTML UI. """
    from regenesis.freeze import freeze_html
    freeze_html()


@manager.command
def analyse():
    from regenesis.analysis import find_denormalized
    find_denormalized()


if __name__ == '__main__':
    manager.run()
