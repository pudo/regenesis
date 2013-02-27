import requests
from lxml import etree

from regenesis.cube import Cube

def fetch_index():
    url = 'https://www.regionalstatistik.de/genesisws/services/RechercheService_2010'
    for i in range(10):
        params = [
            ('method', 'DatenKatalog'),
            ('kennung', ''),
            ('passwort', ''),
            ('filter', '%s*' % i),
            ('bereich', 'Alle'),
            ('listenLaenge', ''),
            ('sprache', 'de')
            ]
        doc = requests.get(url, params=params)
        doc = etree.fromstring(doc.content)
        for entry in doc.findall('.//datenKatalogEintraege/datenKatalogEintraege'):
            yield entry.findtext('./code')

def fetch_cube(name):
    url = 'https://www.regionalstatistik.de/genesisws/services/ExportService_2010'
    params = [
        ('method', 'DatenExport'),
        ('kennung', ''),
        ('passwort', ''),
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
    doc = requests.get(url, params=params)
    doc = etree.fromstring(doc.content)
    data = doc.find('.//quaderDaten').text
    return Cube(name, data)


def main():
    for code in fetch_index():
        cube = fetch_cube(code)
        from pprint import pprint
        pprint(cube.axes)
        return
        #pprint(list(cube.sections['MM'].objects))
        #pprint([f.mapping for f in cube.facts])
        import json
        from regenesis.export import JSONEncoder
        fh = open('exports/%s.json' % cube.name, 'wb')
        json.dump(cube, fh, cls=JSONEncoder, indent=2)
        fh.close()

if __name__ == '__main__':
    #cube = fetch_cube('12613BJ003')
    cube = fetch_cube('52411KJ001')
    from pprint import pprint
    #pprint(cube.facts)
    pprint([f.mapping for f in cube.facts])

    #main()
