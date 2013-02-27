import unittest

import variable
import mongo

class variableTest(unittest.TestCase):
    
    def setUp(self):
        self.db = mongo.get_db()
    
    def test_types(self):
        types = set()
        types_ausp = {}
        for variable in self.db.variables.find():
            #print variable
            #assert False
            typ = variable.get('typ')
            types.add(typ)
            #types_ausp[typ] = types_ausp.get(typ, []) + [variable.get('auspraegungen')]
        print types
    
    

if __name__ == '__main__':
    unittest.main()