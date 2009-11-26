import Queue
import data as data
import simplejson as json
from data import NetworkInQueueItem, NetworkOutQueueItem
from shared.util import getLogger
log = getLogger("server.log")

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
        if self.item_type == data.NetworkInQueueItem:
            return session.query(data.NetworkInQueueItem).filter(data.NetworkInQueueItem.sent == 0).count() == 0
        session.close()

    # Check whether the queue is full
    def _full(self):
        return False

    # Put a new item in the queue
    def _put(self, item):
        '''
        Save the packed data (item) and also repack it with message_id
        before commit to database
        '''
        session = self.db._Session()
        session.add(item)
        session.flush()
        d = json.loads(item.data)
        d["message_id"] = item.id
        item.data = unicode(json.dumps(d))
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

class DatabaseInQueue(DatabaseQueue):
    def __init__(self, database):
        DatabaseQueue.__init__(self, database, DatabaseQueue.direction_in)

    def _empty(self):
        session = self.db._Session()
        result = session.query(data.NetworkInQueueItem).filter(data.NetworkInQueueItem.sent == 0).count() == 0
        session.close()
        return result

    def peek(self, message_id):
        session = self.db._Session()
        item = session.query(data.NetworkInQueueItem).filter(data.NetworkInQueueItem.id == message_id).first()
        session.close()
        if item is not None:
            return item.data
        else:
            return None

    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument
    def put(self, data, priority=0, block=True, timeout=None):
        item = data, priority
        item = NetworkInQueueItem(data, priority)
        log.debug("putting:" + data)
        Queue.Queue.put(self, item, block, timeout)
        return item.id



class DatabaseOutQueue(DatabaseQueue):
    name = None
    def __init__(self, database, name):
        DatabaseQueue.__init__(self, database, DatabaseQueue.direction_out)
        self.name = name

    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument
    def put(self, data, priority=0, block=True, timeout=None):
        item = data, priority
        item = NetworkOutQueueItem(data, priority)
        log.debug("putting:" + data)
        Queue.Queue.put(self, self.name, item, block, timeout)
        return item.id


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
