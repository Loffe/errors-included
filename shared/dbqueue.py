import Queue
import shared.data as data

class DatabaseQueue(Queue.Queue):
    direction_in, direction_out = range(2)

    def __init__(self, database, direction):
        Queue.Queue.__init__(self)
        self.item_type = [data.NetworkInQueueItem, data.NetworkOutQueueItem][direction]
        self.db = database
        self.session = database._Session()

    # Return the number of items that are currently enqueued
    def _qsize(self):
        # @TODO
        return 2

    # Check whether the queue is empty
    def _empty(self):
        if self.item_type == data.NetworkOutQueueItem:
            return self.session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.sent == 0).count()

    # Check whether the queue is full
    def _full(self):
        return False

    # Put a new item in the queue
    def _put(self, (data, prio)):
        item = self.item_type(data, prio)
        self.session.add(item)
        self.session.commit()

    # Get an item from the queue
    def _get(self):
        # @TODO
        print "_get"
        if self.item_type == data.NetworkOutQueueItem:
            q = self.session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.sent == False)
            return q.first()
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
        item.sent = True
        self.session.commit()
