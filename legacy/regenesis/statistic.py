from datetime import datetime
import urllib2, urllib
from BeautifulSoup import BeautifulSoup
import logging
import soap
import config
import scrape
import mongo

def get(stat_id, include_tables=True):
    db = mongo.get_db()
    statistic = db.statistics.find_one({'code': stat_id})
    if (not statistic) or config.bool('reload'):
        logging.info("Statistic %s not found, loading from SOAP...", stat_id)
        statistic = soap.get_statistic(stat_id)
        if not statistic: 
            return None
        tables = []
        for table in soap.find_tables_by_statistic(stat_id):
            tables.append(table)
        statistic['tables'] = tables
        statistic['description'] = load_description(stat_id)
        statistic['variables'] = [v for v in load_variables(stat_id)]
        statistic['__ts'] = datetime.utcnow()
        db.statistics.update({'code': stat_id}, statistic, upsert=True)
    import table
    for _table in statistic['tables']:
        table.get(_table.get('code'))
    return statistic


def load_description(stat_id):
    url = config.url("?sequenz=statistikInfo&selectionname=%s&sprache=de" % stat_id)
    soup = BeautifulSoup(urllib2.urlopen(url))
    texte = soup.findAll(attrs={'class': 'langtext'})
    text = u'\n'.join([t.contents[0] if len(t.contents) else '\n' for t in texte])
    return text


def load_variables(stat_id):
    url = config.url("?sequenz=statistikMerkmale&selectionname=%s&sprache=de" % stat_id)
    for tr in scrape.read_table_pages(url):
        td = tr.find('td')
        if td:
            yield td.find('div').contents[0]


def all(include_tables=True):
    for i in range(11111, 99999):
        #print "i = %s" % i
        try:
            get(str(i), include_tables=include_tables)
        except Exception, e:
            logging.exception(e)
    
