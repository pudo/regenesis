import os
import json
from regenesis.core import app

def cube_path(catalog, cube_name, ext='raw'):
    return os.path.join(
            app.config.get('DATA_DIRECTORY'),
            catalog,
            cube_name + '.' + ext
            )

def exists_raw(catalog, cube_name):
    return os.path.isfile(cube_path(catalog, cube_name))

def store_cube_raw(catalog, cube_name, cube_data):
    path = cube_path(catalog, cube_name)
    if not os.path.isdir(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    fh = open(path, 'wb')
    fh.write(cube_data.encode('utf-8'))
    fh.close()

def load_cube_raw(catalog, cube_name):
    fh = open(cube_path(catalog, cube_name), 'rb')
    data = fh.read().decode('utf-8')
    fh.close()
    return data

def dump_cube_json(catalog, cube):
    fh = open(cube_path(catalog, cube.name, 'json'), 'wb')
    json.dump(cube, fh, cls=JSONEncoder, indent=2)
    fh.close()

