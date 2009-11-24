
class IDProvider(object):
    INTERVAL = 1000
    next_interval_start = 1
    database = None

    def __init__(self, database):
        self.database = database

    def provide(self):
        print "providing"
