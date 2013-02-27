from datetime import datetime
import logging
import soap
import config
import scrape
import mongo
import util

def get(code):
    db = mongo.get_db()
    variable = db.variables.find_one({'code': code})
    if (not variable) or config.bool('reload'):
        logging.info("Variable %s not found, loading from SOAP...", code)
        variable = soap.get_variable(code)
        if not variable: 
            return None
        for link in variable.get('links', []):
            if u"Tabellen mit Vorkommen des Merkmals" in link.get('titel'):
                variable['tables'] = [t for t in load_variable_tables(link.get('href'))]
        variable['__ts'] = datetime.utcnow()
        db.variables.update({'code': code}, variable, upsert=True)
    return variable


def load_variable_tables(href):
    for tr in scrape.read_table_pages(href):
        yield tr.find('a').get('id')

       
def all():
    def _generate():
        for tr in scrape.read_table_pages(config.url("?operation=merkmaleVerzeichnis")):
            td = tr.find('td')
            if not td: continue
            if td.string:
                #print td.string.encode('utf-8')
                yield td.string.encode('utf-8')
            else:
                yield td.find('a').get('id').encode('utf-8')
    
    [get(i) for i in _generate()]
    #util.run_threaded(_generate(), get, num_threads=1)
