#!/usr/bin/jython
"""Unit tests for the mysql interface"""

import unittest
from t_mysql import *

class TestSequenceFunctions(unittest.TestCase): 
    def setUp(self):
        self.db = MySQLAccess()

    def gen_to_list(self, gen):
        return gen.make_into_list()

    def sequential_inserter(self, width):
        """Generator needs to be setup before calling this."""
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

    def insert_query_all(self, width):
        """Test sequential inserting and query_all for 101 records in 101 
        streams. Because MySQL does not place a guarantee on query return 
        order, this test is rather slow."""
        gen = self.db.init_insert(101, 101, width, True)
        compareresult = self.gen_to_list(gen)
        self.sequential_inserter(width)

        #compareresult.pop(0) #test the test
        #compareresult += ['LOL'] #test the test 
        result = self.db.run_query_all(debug=True)
        if False:
            print(result)
            print(compareresult)

        self.assertEqual(len(result), len(compareresult))
        for x in compareresult:
            self.assert_(x in result)

    def test_query_all_width(self):
        """A simultaneous test of query_all and width-wise sequential 
        insertion."""
        self.db = MySQLAccess()
        self.insert_query_all(True)
    
    def test_query_all_height(self):
        """A simultaneous test of query_all and height-wise sequential
        insertion."""
        self.db = MySQLAccess()
        self.insert_query_all(False)

    def test_query(self):
        """Test query over a range of records/streams"""
        # want to check 1) length of result and 2) that all values in result 
        # are in the generator, although it would be pretty hard for them not
        # to be
        width = True #we'll only do one here since it really doesn't matter
        self.db = MySQLAccess()
        gen = self.db.init_insert(101, 101, width, True)
        compareresult = self.gen_to_list(gen)
        self.sequential_inserter(width)

        result = self.db.query(10, 10, True)
        
    
    def test_query_single(self):
        """Test query of a single stream"""
        pass
        


if __name__== '__main__':
    unittest.main()
