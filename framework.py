from random import choice
import time

class TSdata_w(object):
    """A 'width-wise' generator for timeseries data.
    Each call to next produces a list of 3 tuples with one record for the entire
    stream range. Effectively iterates over points.

    """
    def __init__(self, num_pts, num_streams, values_range):
        """ Initialize the tsdata generator
        Args:
        num_pts -- the number of points to generate before raising StopIteration
        num_streams -- number of streams to generate per point
        values_range -- range(...) of valid values
        """
        self.num_pts = num_pts
        self.pt_time = 946684800 #start on Jan 1, 2000 @ 00:00:00
        self.streams = range(1, num_streams+1)
        self.valid_values = values_range
        self.currentstream = 1

    def __iter__(self):
        return self
    
    def next(self):
        """ Returns a list of 3-tuples of (streamid, time, point) of length
        num_streams."""
        out = []
        if self.num_pts > 0:
            for st_id in self.streams:
                out.append((st_id, self.pt_time, choice(self.valid_values)))
            self.num_pts -= 1
            self.pt_time += 1
            return out
        else:
            raise StopIteration()

class TSdata_h(TSdata_w):
    """A 'height-wise' generator for timeseries data.
    Each call to next produces a list of 3 tuples with num_pts number of records
    for one stream in the stream range. Effectively iterates over streams."""
    
    def next(self):
        """ Returns a list of 3-tuples of (streamid, time, point) of length
        num_points."""
        out = []
        ptime = self.pt_time
        if self.currentstream in self.streams:
            for pt in range(self.num_pts):
                out.append((self.currentstream, self.pt_time, 
                                                    choice(self.valid_values)))
                self.pt_time += 1
            self.currentstream += 1
            return out
        else:
            raise StopIteration()


class DBTest(object):
    """ A pseudo-interface for DB tests (zope.interface is incompatible 
    with jython). Essentially we want to implement the most optimized 
    query for each DB in subclasses of this. Ultimately, this may be wrapped in
    grinder's logger system."""

    def __init__(self):
        """Here, we need to start connections, etc"""
        pass

    ### These are abstractions for SQL/other queries
    ### When a test is complete, these should raise a StopIteration from the
    ### TSdata generator.
    
    def init_insert(self, records, streams, width=True):
        """Initialize an insertion test, return string describing the test."""
        if width:
            self.insertGenerator = TSdata_w(records, streams, range(80, 120, 1))
        else:
            self.insertGenerator = TSdata_h(records, streams, range(80, 120, 1))
        returnstr = ("Started Logging: " + str(records) + " records each for " + 
                        str(streams) + " streams at " + str(time.time()) + 
                            " seconds since the epoch.")
        return returnstr

    def run_insert_w(self):
        """Run one round of an insertion test. This will be implemented by a
        subclass. This is width-wise, but the distinction is only relevant for
        readingdb"""
        pass

    def run_insert_h(self):
        """Same as run_insert_w() except for in readingdb. So it's overridden
        only in readingdb ATM."""
        return self.run_insert_w()

    def append(self, val, streams):
        """Append a single value (val) to "streams" streams"""
        pass

    def run_query_all(self):
        """Query all records in the table"""
        pass

    def query(self, records, streams):
        """Query "records" records from "streams" streams"""
        pass

    def querylast(self, records, streams):
        """Get last "records" records for "streams" streams"""
        pass

    def prepare(self):
        """Here, include any actions that prepare the database, including:
        -clearing database cache
        -clearing filesystem cache
        This will be called by __init__.
        """
        pass

def importstrs(dbname):
    d2imp = {'mysql': 'from t_mysql import MySQLAccess', 'postgres': 
                'from t_postgres import PostgresAccess', 'readingdb': 
                'from t_readingdb import ReadingDBAccess'}

    out = d2imp[dbname]
    out += ' as DBAccess'
    return out
