
DEBUG = True

ETL_URL = 'postgresql://localhost/regenesis'
DATA_DIRECTORY = 'exports/'

API_ENDPOINT = 'http://api.regenesis.pudo.org'

CATALOG = {
    'regional': {
        'title': 'Regionalstatistik',
        'url': 'https://www.regionalstatistik.de/',
        'username': '',
        'password': '',
        'export_url': 'https://www.regionalstatistik.de/genesisws/services/ExportService_2010',
        'index_url': 'https://www.regionalstatistik.de/genesisws/services/RechercheService_2010'
    }
}
