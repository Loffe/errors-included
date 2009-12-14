import Queue
import re
import data as data
import simplejson as json
from data import NetworkInQueueItem, NetworkOutQueueItem
from shared.util import getLogger, print_color
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
            print "sending few (no) messages!"
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
        if item.__class__ == NetworkOutQueueItem and \
                "\"subtype\": \"change\"" in item.data:
            ''' Check for old events for the same unit and remove them.
                This will speedup the startup of clients.
            '''
            res = re.findall(r'"id": (\d*)', item.data)
            assert len(res) == 1
            id = res[0]
            #print "dumping old changes for id:", id
            res = session.query(NetworkOutQueueItem).filter_by(name=self.name, sent=0)
            to_del = []
            for row in res:
                # Remove old change events
                match1 = re.findall(r'"subtype": "change"', row.data)
                match2 = re.findall(r'"id": %s' % id, row.data)
                if len(match1) > 0 and len(match2) > 0:
                    #print_color(str(row), 'red')
                    to_del.append(str(row.id))

                # Remove old service levels
                match_service_level = re.findall(r'"type": "service_level"', row.data)
                if len(match_service_level) > 0:
                    to_del.append(str(row.id))
            #print "to_del", to_del
            if len(to_del) > 0:
                session.execute("DELETE FROM OutQueue WHERE id IN (" + ",".join(to_del) + ")")
            #print "to_add", item.data
        session.add(item)
        session.flush()
        try:
            d = json.loads(item.data)
            d["message_id"] = item.id
            item.data = unicode(json.dumps(d))
        except ValueError, e:
            print_color("not a valid json string. Trunkated by TCP?", 'red')
        except TypeError, e:
            print "Stop being stupid"
            print type(d), item.id
        session.add(item)
        session.commit()
        session.close()

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
        result = session.query(data.NetworkInQueueItem).filter(data.NetworkInQueueItem.processed == 0).count() == 0
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

    def mark_as_processed(self, id):
        # @TODO: acuire lock maybe?
        session = self.db._Session()
        q = session.query(data.NetworkInQueueItem).filter_by(id = id)
        item = q.first()
        item.processed = True
        session.commit()
        session.close()

    def mark_as_failed(self, id, error_code = 2):
        print_color("marking %d as failed" % id, 'red')
        # @TODO: acuire lock maybe?
        session = self.db._Session()
        q = session.query(data.NetworkInQueueItem).filter_by(id = id)
        item = q.first()
        item.processed = error_code
        session.commit()
        session.close()

    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument
    def put(self, data, priority=0, block=True, timeout=None):
        item = data, priority
        item = NetworkInQueueItem(unicode(data), priority)
        log.debug("putting:" + data)
        Queue.Queue.put(self, item, block, timeout)
        return item.id

    def _get(self):
        # @TODO
        session = self.db._Session()
        print "_get"
        q = session.query(NetworkInQueueItem).filter_by(processed = False)
        item = q.first()
        session.close()
        return item.data, item.id

class DatabaseOutQueue(DatabaseQueue):
    name = None
    service_level = None
    
    def __init__(self, database, name):
        DatabaseQueue.__init__(self, database, DatabaseQueue.direction_out)
        self.name = name

    def set_service_level(self, level):
        self.service_level = level

    def _empty(self):
        session = self.db._Session()
        result = None
        if self.service_level == "send-few" or self.service_level == "energysaving":
            q = session.query(NetworkOutQueueItem).filter_by(sent = False) \
                    .filter_by(name = self.name) \
                    .filter("prio>=5") \
                    .order_by(NetworkOutQueueItem.prio.desc()) \
                    .order_by(NetworkOutQueueItem.id.asc()).count()
            result = (q == 0)
            #row = session.execute("SELECT COUNT(*) AS num FROM OutQueue WHERE name = '%s' AND sent = 0 AND prio >= 5" % (self.name)).fetchone()
            #result = row[0] == 0
        else:
            result = session.query(NetworkOutQueueItem).filter_by(sent = 0).filter_by(name=self.name).count() == 0
        session.close()
        return result

    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument
    def put(self, data, priority=0, block=True, timeout=None):
        item = data, priority
        item = NetworkOutQueueItem(self.name, unicode(data), priority)
        log.debug("putting:" + data)
        Queue.Queue.put(self, item, block, timeout)
        return item.id

    # Get an item from the queue
    def _get(self):
        session = self.db._Session()
        if self.service_level == "send-few" or self.service_level == "energysaving":
            q = session.query(NetworkOutQueueItem).filter_by(sent = False) \
                    .filter_by(name = self.name) \
                    .filter("prio>=5") \
                    .order_by(NetworkOutQueueItem.prio.desc()) \
                    .order_by(NetworkOutQueueItem.id.asc())
        else:
            q = session.query(NetworkOutQueueItem).filter_by(sent = False) \
                    .filter_by(name = self.name) \
                    .order_by(NetworkOutQueueItem.prio.desc()) \
                    .order_by(NetworkOutQueueItem.id.asc())
        item = q.first()
        session.close()
        if item is None:
            raise IndexError, "No such item i queue"
        return item.data, item.id

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
