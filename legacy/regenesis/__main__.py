from pprint import pprint
import sys
import time
import logging

def test_load():
    begin = time.time()
    #import variable
    #variable.all()
    import soap
    #print soap.get_statistic('11111')
    #soap.get_statistic('183')
    #logging.info(soap.get_table_meta('11111-0001'))
    #soap.get_variable('ERW006')
    import statistic
    #statistic.all()
    #statistic.get('11111')
    #statistic.get('43311')
    #statistic.get('52311')
    #print soap.get_variable('ADSST2', var_name='code')
    pprint(soap.find_tables_by_statistic('11111'))
    
    import table
    #pprint(table.get('12211-0007'))
    #table.get('21411-0001', force_reload=True)
    #table.get('43311-0001', force_reload=True)
    #table.get('12211-0104', force_reload=True)
    
    #logging.info(table.get('12211-0104', force_reload=True))
    
    #run_once()
    print "TIME: %s" % (time.time() - begin)
    
def run_once():
    import terms
    terms.load_terms()
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    #logging.getLogger('suds').setLevel(logging.ERROR)
    if sys.argv[1] == 'variables':
        import variable 
        variable.all()
    elif sys.argv[1] == 'variable':
        import variable
        pprint(variable.get(sys.argv[2]))
    elif sys.argv[1] == 'table':
        import table
        pprint(table.get(sys.argv[2]))
    elif sys.argv[1] == 'statistic':
        import statistic
        pprint(statistic.get(sys.argv[2]))
    elif sys.argv[1] == 'load':
        import statistic
        statistic.all()
    elif sys.argv[1] == 'test':
        test_load()
