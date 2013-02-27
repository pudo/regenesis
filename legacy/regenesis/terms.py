from datetime import datetime
import scrape
import config
from mongo import get_db

def terms_it():
    for tr in scrape.read_table_pages(config.url("?operation=begriffeVerzeichnis")):
        yield tr.findAll('a')[0].get('id')

def load_terms():
    db = get_db()
    for term in terms_it():
        db.terms.update({'term': term}, 
                        {'term': term, '__ts': datetime.utcnow()},
                        upsert=True)
        