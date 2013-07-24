import logging
import warnings;
warnings.filterwarnings('ignore', 'Unicode type received non-unicode bind param value.')
from sqlalchemy.exc import SAWarning
warnings.filterwarnings('ignore', category=SAWarning)

from flask import Flask
import dataset

from regenesis import default_settings

app = Flask(__name__)
app.config.from_object(default_settings)
app.config.from_envvar('REGENESIS_SETTINGS', silent=True)

engine = dataset.connect(app.config.get('ETL_URL'))

logging.basicConfig(level=logging.INFO)


def get_catalog(catalog_name):
    catalog = app.config.get('CATALOG').get(catalog_name)
    if catalog is None:
        raise ValueError('No such catalog: %s' % catalog_name)
    catalog['name'] = catalog_name
    return catalog
