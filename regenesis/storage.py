import os
import json
from regenesis.core import app

def cube_path(cube_name, ext):
    return os.path.join(
            app.config.get('DATA_DIRECTORY'),
            cube_name + '.' + ext
            )

def exists_raw(cube_name):
    return os.path.isfile(cube_path(cube_name, 'raw'))

def store_cube_raw(cube_name, cube_data):
    fh = open(cube_path(cube_name, 'raw'), 'wb')
    fh.write(cube_data.encode('utf-8'))
    fh.close()

def load_cube_raw(cube_name):
    fh = open(cube_path(cube_name, 'raw'), 'rb')
    data = fh.read().decode('utf-8')
    fh.close()
    return data

def dump_cube_json(cube):
    fh = open(cube_path(cube.name, 'json'), 'wb')
    json.dump(cube, fh, cls=JSONEncoder, indent=2)
    fh.close()

