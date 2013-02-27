from datetime import datetime

import config
from pymongo import Connection
from threading import local


def get_db():
    l = local()
    if not l.__dict__.get('db'):
        conn = Connection()
        l.__dict__['db'] = conn[config.get('db')]
    return l.__dict__['db']
    
EMPTY = '____EMPTY____'
    
def cache_result(data, **kwargs):
    record = dict(kwargs.items())
    record['__ts'] = datetime.utcnow()
    if not data:
        data = EMPTY
    record['__data'] = data
    record['section'] = config.section()
    get_db().loadcache.update(kwargs, record, upsert=True)
    
def load_cached(**kwargs):
    if config.bool('cache'):
        kwargs['section'] = config.section()
        data = get_db().loadcache.find_one(kwargs)
        if data:
            return data.get('__data', {})
