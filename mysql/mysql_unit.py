#!/usr/bin/jython
"""Unit tests for the mysql interface"""

import unittest
from t_mysql import *

class TestSequenceFunctions(unittest.TestCase): 
    def setUp(self):
        self.db = MySQLAccess() 

    def insert_query_small(self, width):
        """Test inserting and querying for 10 records. Because MySQL does not 
        place a guarantee on query return order, this test is rather slow."""
        gen = self.db.init_insert(100, 100, width, True)
        unpack = lambda x: x[0]
        form = lambda x: list(x[:2])
        compareresult = map(form, sum(map(unpack, map(list, list(gen))), []))
        #compareresult.pop(0) #test the test
        #compareresult += ['LOL'] #test the test 
        while True:
            try:
                self.db.run_insert_w()
            except StopIteration:
                print("Insertion Completed")
                break
            except:
                print("An error occurred during the insertion")
                break
        result = self.db.run_query_all(debug=True)
        self.assertEqual(len(result), len(compareresult))
        for x in compareresult:
            self.assert_(x in result)

    def test_insert_query_small_width(self):
        self.db = MySQLAccess()
        self.insert_query_small(True)
    
    def test_insert_query_small_height(self):
        self.db = MySQLAccess()
        self.insert_query_small(False)
        


if __name__== '__main__':
    unittest.main()
