import time
import urllib2, urllib
from BeautifulSoup import BeautifulSoup
from mongo import cache_result, load_cached
import pickle

def read_table_pages(url):
    class Request(urllib2.Request):
        def get_method(self): return 'POST'

    while True:
        ph = urllib2.urlopen(url)
        page = ph.read()
        ph.close()
        #if not 'verzeichnis' in page and not 'vorhanden' in page:
        #    print "Fetch failure, retry in 1 sec."
        #    time.sleep(1)
        #    continue
        soup = BeautifulSoup(page)
        tables = soup.findAll('table', attrs={'class': 'verzeichnis'})
        if not len(tables):
            break
        rows = tables[0].findAll('tr')[::-1][1:]
        if not len(rows):
            break
        for row in rows:
            yield row
        if 'blaettern' in page:
            form = soup.findAll('form', attrs={'name': 'blaetternOben'})[0]
            url = Request(form.get('action'), 'forward.x=42&forward.y=23', {}) 
        else: break