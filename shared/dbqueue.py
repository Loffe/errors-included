import Queue
import data as data

class DatabaseQueue(Queue.Queue):
    direction_in, direction_out = range(2)

    def __init__(self, database, direction):
        Queue.Queue.__init__(self)
        self.item_type = [data.NetworkInQueueItem, data.NetworkOutQueueItem][direction]
        self.db = database
        self.session = database._Session()
        self.read_session = database._Session()

    # Return the number of items that are currently enqueued
    def _qsize(self):
        # @TODO
        return 2

    # Check whether the queue is empty
    def _empty(self):
        session = self.db._Session()
        if self.item_type == data.NetworkOutQueueItem:
            return session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.sent == 0).count() == 0

    # Check whether the queue is full
    def _full(self):
        return False

    # Put a new item in the queue
    def _put(self, (data, prio)):
        session = self.db._Session()
        item = self.item_type(data, prio)
        session.add(item)
        session.commit()

    # Get an item from the queue
    def _get(self):
        # @TODO
        print "_get"
        if self.item_type == data.NetworkOutQueueItem:
            q = self.read_session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.sent == False)
            return q.first().data
        print "nope, don't think so"
        return None

    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument
    def put(self, data, priority=0, block=True, timeout=None):
        item = data, priority
        Queue.Queue.put(self, item, block, timeout)

    # shadow and wrap Queue.Queue's own `get' to strip auxiliary aspects
    #def get(self, block=True, timeout=None):
        #priority, time_posted, item = Queue.Queue.get(self, block, timeout)
        #return item

    def mark_as_sent(self, item):
        session = self.db._Session()
        item.sent = True
        session.commit()


if __name__ == "__main__":
    import data
    db = data.create_database()
    queue = DatabaseQueue(db, DatabaseQueue.direction_out)
    _data = "{\"data\": 123}"
    queue.put(_data, 4)
    while True:
        data2 = queue.get(block=False)
        print data2
        queue.mark_as_sent(data2)
        print data2
    print "Finished"
