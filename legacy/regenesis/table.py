from pprint import pprint
from datetime import datetime
import os
from itertools import repeat
import urllib2, urllib
from BeautifulSoup import BeautifulSoup
from pprint import pprint
import logging
import soap
import scrape
import config
import mongo
import codecs
from copy import copy
import variable


TABLE_SETUP_KEYS = {
    'Globale Angaben': 'global', 
    'Kopfzeile': 'top',
    'Vorspalte': 'pre',
    'Untertitel': 'pre',
    'Zwischentitel': 'pre'
}

from table_parser import tableParser

def get(table_id):
    db = mongo.get_db()
    table = db.tables.find_one({'code': table_id})
    if (not table) or config.bool('reload'):
        logging.info("Table %s not found, loading from SOAP...", table_id)
        table_data = soap.get_table(table_id)
        if not table_data: 
            return None
        get_data(table_id)
        table = {'csvdata': table_data, 'code': table_id}
        table.update(table_to_dict(table_id, table_data))
        db.tables.update({'code': table_id}, table, upsert=True)        
    else:
        reparse_table(table_id)
    return table


def get_data(table_id):
    if not config.get("data_path"):
        return
    for format in ["csv", "html"]:
        data = soap.get_table(table_id, format=format)
        if data:
            fn = os.path.join(config.get("data_path"), "table_%s.%s" % (table_id, format)) 
            out_file = codecs.open(fn, "w", "utf-8")
            out_file.write(data)
            out_file.close()


def for_statistic(statistic_id):
    statistic = db.statistics.find_one({'code': statistic_id})
    for table in statistic['tables']:
        get(table.get('code'))


def _generate_all_tables():
    for statistic in db.statistics.find():
        for table in statistic['tables']:
            yield table.get('code')
        
        
def all():
    for table_id in _generate_all_tables():
        try:
            get(table_id)
        except Exception, e:
            logging.exception(e)


def table_to_dict(table_id, table_data):
    return {}
    try:
        s, v = load_structure(table_id)
        tp = tableParser(s, v, table_data)
        tp.parse()
        data = tp.to_dict()
        
        #for cell in data.get('cells', []):
        #    cell['table'] = table_id
        #    db.cells.insert(cell)      
        return data
    except Exception, e:
        logging.error("ERROR IN %s -----" % table_id)
        logging.exception(e)
        return {}


def reparse_table(table_id):
    db = mongo.get_db()
    table = db.tables.find_one({'code': table_id})
    #print table.get('csvdata').encode('utf-8')
    print "TABLE", table_id
    print table.get('csvdata', '').encode('utf-8')
    
    table.update(table_to_dict(table_id, table.get('csvdata')))
    db.tables.update({'code': table_id}, table, upsert=True)


def reparse_all():
    for table_id in _generate_all_tables():
        reparse_table(table_id)


def load_structure(table_id):
    # TODO Return trees, not dict
    setup = {'global': [], 'top': [], 'pre': []}
    vars = []
    ph = urllib2.urlopen(config.url("?sequenz=tabelleAufbau&selectionname=%s&sprache=de" % table_id))
    soup = BeautifulSoup(ph.read())
    ph.close()
    table = soup.find('div', attrs={'class': 'ContentRegion'}).findAll('table')[1]
    for row in table.findAll('tr', recursive=False):
        columns = row.findAll('td', recursive=False)
        if not len(columns):
            continue
        variable = columns[1].contents[0]
        pos = TABLE_SETUP_KEYS.get(columns[0].find('a')['title'])
        
        name_titles = columns[2].findAll('img')
        indent = len([t for t in name_titles if t['title'] == 'Unterordnung'])
        setup[pos] = setup[pos] + [(variable, indent)]
        vars.append(variable)
    return setup, vars
  


                
        