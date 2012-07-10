from random import choice

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

    ### These are abstractions for SQL/other queries
    def insert(self, records, streams):
        """Insert "records" records into "streams" streams"""
        self.prepare()
        pass

    def append(self, val, streams):
        """Append a single value (val) to "streams" streams"""
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
    d2imp = {'mysql': 'from t_mysql import MySQLAccess'}

    out = d2imp[dbname]
    out += ' as DBAccess'
    return out
