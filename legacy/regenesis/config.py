import ConfigParser
import os


config = ConfigParser.SafeConfigParser()
config.read(['genesis.cfg'])


def section():
    return config.get("DEFAULT", "section")

def get(key):
    try:
        return config.get(section(), key)
    except ConfigParser.NoOptionError:
        return None
    
def bool(key):
    return config.get(section(), key) in ["true", "True", "yes", "1"]
    
def url(part):
    return get('base_url') + part