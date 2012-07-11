from random import choice
import time

class TSdata(object):
    """A generator for timeseries data."""
    def __init__(self, num_pts, num_streams, values_range):
        """ Initialize the tsdata generator
        Args:
        num_pts -- the number of points to generate before raising StopIteration
        num_streams -- number of streams to generate per point
        values_range -- range(...) of valid values
        """
        self.num_pts = num_pts
        self.pt_time = 946684800 #start on Jan 1, 2000 @ 00:00:00
        self.streams = range(num_streams)
        self.valid_values = values_range

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
    
    def init_insert(self, records, streams):
        """Initialize an insertion test, return string describing the test."""
        self.insertGenerator = TSdata(records, streams, range(80, 120, 1))
        returnstr = ("Started Logging: " + str(records) + " records each for " + 
                        str(streams) + " streams at " + str(time.time()) + 
                            "seconds since the epoch.")
        return returnstr

    def run_insert(self):
        """Run one round of an insertion test. This will be implemented by a
        subclass."""
        pass

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
                'from t_postgres import PostgresAccess'}

    out = d2imp[dbname]
    out += ' as DBAccess'
    return out
