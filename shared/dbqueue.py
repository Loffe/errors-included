import Queue
import data as data

class DatabaseQueue(Queue.Queue):
    direction_in, direction_out = range(2)

    def __init__(self, database, direction):
        Queue.Queue.__init__(self)
        self.item_type = [data.NetworkInQueueItem, data.NetworkOutQueueItem][direction]
        self.db = database

    # Return the number of items that are currently enqueued
    def _qsize(self):
        # @TODO
        return 2

    # Check whether the queue is empty
    def _empty(self):
        session = self.db._Session()
        if self.item_type == data.NetworkOutQueueItem:
            return session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.sent == 0).count() == 0
        session.close()

    # Check whether the queue is full
    def _full(self):
        return False

    # Put a new item in the queue
    def _put(self, (data, prio)):
        session = self.db._Session()
        item = self.item_type(data, prio)
        session.add(item)
        session.commit()
        session.close()

    # Get an item from the queue
    def _get(self):
        # @TODO
        session = self.db._Session()
        print "_get"
        if self.item_type == data.NetworkOutQueueItem:
            q = session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.sent == False)
            item = q.first()
            return item.data, item.id
        print "nope, don't think so"
        session.close()
        return None

    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument
    def put(self, data, priority=0, block=True, timeout=None):
        item = data, priority
        Queue.Queue.put(self, item, block, timeout)

    # shadow and wrap Queue.Queue's own `get' to strip auxiliary aspects
    def get(self, block=True, timeout=None):
        item, id = Queue.Queue.get(self, block, timeout)
        return item, id

    def mark_as_sent(self, id):
        # @TODO: acuire lock maybe?
        session = self.db._Session()
        q = session.query(data.NetworkOutQueueItem).filter(data.NetworkOutQueueItem.id == id)
        item = q.first()
        item.sent = True
        session.commit()
        session.close()


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
