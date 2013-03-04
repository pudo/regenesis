import requests
from lxml import etree

from regenesis.cube import Cube

def fetch_index(catalog):
    for i in range(10):
        params = [
            ('method', 'DatenKatalog'),
            ('kennung', catalog.get('username')),
            ('passwort', catalog.get('password')),
            ('filter', '%s*' % i),
            ('bereich', 'Alle'),
            ('listenLaenge', ''),
            ('sprache', 'de')
            ]
        doc = requests.get(catalog.get('index_url'), params=params)
        doc = etree.fromstring(doc.content)
        for entry in doc.findall('.//datenKatalogEintraege/datenKatalogEintraege'):
            yield entry.findtext('./code')

def fetch_cube(catalog, name):
    params = [
        ('method', 'DatenExport'),
        ('kennung', catalog.get('username')),
        ('passwort', catalog.get('password')),
        ('namen', name),
        ('bereich', 'Alle'),
        ('format', 'csv'),
        ('werte', True),
        ('metadaten', True),
        ('zusatz', True),
        ('startjahr', ''),
        ('endjahr', ''),
        ('zeitscheiben', ''),
        ('inhalte', ''),
        ('regionalmerkmal', ''),
        ('regionalschluessel', ''),
        ('sachmerkmal', ''),
        ('sachschluessel', ''),
        ('sachmerkmal2', ''),
        ('sachschluessel2', ''),
        ('sachmerkmal3', ''),
        ('sachschluessel3', ''),
        ('stand', ''),
        ('sprache', 'de')
        ]
    doc = requests.get(catalog.get('export_url'), params=params)
    doc = etree.fromstring(doc.content)
    return doc.find('.//quaderDaten').text
    #return Cube(name, data)

