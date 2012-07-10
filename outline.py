

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


