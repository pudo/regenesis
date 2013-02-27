
from threading import local
from suds.client import *
from suds import *

import config
from mongo import cache_result, load_cached, EMPTY
from util import serialize_soap

def get_test_service():
    d = local()
    if d.__dict__.get('test') is None:
        d.__dict__['test'] = Client(config.get('test_service'))
    return d.__dict__.get('test')

def get_recherche_service():
    d = local()
    if d.__dict__.get('recherche') is None:
        d.__dict__['recherche'] = Client(config.get('recherche_service'))
    return d.__dict__.get('recherche')

def get_download_service():
    d = local()
    if d.__dict__.get('download') is None:
        d.__dict__['download'] = Client(config.get('download_service'), retxml=True)
    return d.__dict__.get('download')    

def get_export_service():
    d = local()
    if d.__dict__.get('export') is None:
        d.__dict__['export'] = Client(config.get('export_service'))
    return d.__dict__.get('export')


def get_statistic(stat_id):
    statistic = load_cached(stat_id=stat_id, _type='statistic')
    if not statistic:
        service = get_recherche_service().service
        data = service.StatistikKatalog(config.get('user'), config.get('password'), 
                                        stat_id, "", "100", config.get('lang'))
        #print data
        if data.objektKatalogEintraege:
            statistic = serialize_soap(data.objektKatalogEintraege[0])
        cache_result(statistic, stat_id=stat_id, _type='statistic')
    elif statistic == EMPTY:
        return None
    return statistic
 
    
def get_table_meta(table_id):
    table = load_cached(table_id=table_id, _type='table_meta')
    if not table:
        service = get_recherche_service().service
        data = service.TabellenKatalog(config.get('user'), config.get('password'), 
                                        table_id, "", "100", config.get('lang'))
        #print data
        if data.objektKatalogEintraege:
            table = serialize_soap(data.objektKatalogEintraege[0])
        cache_result(table, table_id=table_id, _type='table_meta')
    elif table == EMPTY:
        return None
    return table

    
def get_table(table_id, transposed=False, format="csv", from_year=1800, to_year=2100):
    table = load_cached(table_id=table_id, transposed=False, format=format, 
                        from_year=1800, to_year=2100, _type='table')
    if not table:
        service = get_download_service().service
        try:
            #table = service.TabellenDownload(config.get('user'), config.get('password'), table_id, "All", 
            #                                 format, False, transposed, str(from_year), str(to_year), 
            #                                 "*", "*", "*", "*", "*", "*", "*", "*", "*", False, "", 
            #                                 config.get('lang'))
            table = service.TabellenDownload(config.get('user'), config.get('password'), table_id, "Alle", 
                                             format, False, str(from_year), str(to_year), 
                                             "*", "*", "*", "*", "*", "*", "*", "*", "*", False, "", 
                                             config.get('lang'))
            parts = table.split(table.split("\r\n")[1])
            csv = parts[2].split("\r\n\r\n", 1)[-1]
            table = unicode(csv.decode('latin-1'))
        except WebFault, wf:
            #print wf
            table = None
        cache_result(table, table_id=table_id, transposed=False, format=format, 
                            from_year=1800, to_year=2100, _type='table')
    elif table == EMPTY:
        return None
    return table


def find_tables_by_statistic(stat_id):
    tables = load_cached(stat_id=stat_id, _type='table_list')
    if not tables:
        service = get_recherche_service().service
        data = service.TabellenKatalog(config.get('user'), config.get('password'), "%s-*" % stat_id, 
                                       "code", "100", config.get('lang'))
        tables = []
        #print data
        if hasattr(data.objektKatalogEintraege, 'abrufbar'):
            tables.append(serialize_soap(data.objektKatalogEintraege))
        else:
            for t in data.objektKatalogEintraege:
                tables.append(serialize_soap(t)) 
        cache_result(tables, stat_id=stat_id, _type='table_list')
    elif tables == EMPTY:
        return []
    return tables
    
    
def get_variable(var_value, var_name='code'):
    variable = load_cached(var_value=var_value, var_name=var_name, _type='feature')
    if not variable:
        service = get_recherche_service().service
        variable = service.MerkmalsKatalog(config.get('user'), config.get('password'), var_value, 
                                           var_name, "*", "Alle", "100", config.get('lang'), )
        if variable.objektKatalogEintraege:
            variable = serialize_soap(variable.objektKatalogEintraege[0])
            data = service.MerkmalAuspraegungenKatalog(config.get('user'), config.get('password'), 
                                                             variable.get('code'), "*", "", "100", config.get('lang'), )
            if data.merkmalAuspraegungenKatalogEintraege:
                attributes = []
                for e in data.merkmalAuspraegungenKatalogEintraege:
                    attributes.append(serialize_soap(e))
                variable['attributes'] = attributes
        else:
            variable = None
        cache_result(variable, var_value=var_value, var_name=var_name, _type='feature')
    elif variable == EMPTY:
        return None
    return variable

