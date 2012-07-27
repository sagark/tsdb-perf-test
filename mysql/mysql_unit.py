#!/usr/bin/jython
"""Unit tests for the mysql interface"""

import unittest
from t_mysql import *

class TestSequenceFunctions(unittest.TestCase): 
    def setUp(self):
        self.db = MySQLAccess()

    def gen_to_list(self, gen):
        return gen.make_into_list()
        
    def insert_query(self, width):
        """Test sequential inserting and query_all for 101 records in 101 
        streams. Because MySQL does not place a guarantee on query return 
        order, this test is rather slow."""
        gen = self.db.init_insert(101, 101, width, True)
        compareresult = self.gen_to_list(gen)

        #compareresult.pop(0) #test the test
        #compareresult += ['LOL'] #test the test 
        while True:
            try:
                if width:
                    self.db.run_insert_w()
                else:
                    self.db.run_insert_h()
            except StopIteration:
                print("Insertion Completed")
                break
            except:
                print("An error occurred during the insertion")
                break
        result = self.db.run_query_all(debug=True)
        if False:
            print(result)
            print(compareresult)

        self.assertEqual(len(result), len(compareresult))
        for x in compareresult:
            self.assert_(x in result)

    def test_insert_query_width(self):
        self.db = MySQLAccess()
        self.insert_query(True)
    
    def test_insert_query_height(self):
        self.db = MySQLAccess()
        self.insert_query(False)
        


if __name__== '__main__':
    unittest.main()
