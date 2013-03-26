import requests
import re
from lxml import etree
from HTMLParser import HTMLParser

from regenesis.cube import Cube

QUADER = re.compile(r"<quaderDaten>\* (.*)<\/quaderDaten>", re.S | re.M)

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
        ('startjahr', 1900),
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
    #print [doc.url]
    #doc = etree.fromstring(doc.content)
    #return doc.find('.//quaderDaten').text
    m = QUADER.search(doc.content)
    if m is None:
        return
    return HTMLParser().unescape(m.group(1))
    #return Cube(name, data)

