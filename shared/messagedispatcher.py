import dbus
from shared.util import print_color
from shared.dbqueue import DatabaseInQueue
from shared.data import Message, NetworkInQueueItem


class MessageDispatcher(object):
    connected_ids = {}
    connected_types = {}
    def __init__(self, bus, database, path="included.errors.Client"):
        self.db = database
        self.connect_to_dbus(bus, path)
        self.queue = DatabaseInQueue(database)

    def connect_to_id(self, id, callback):
        self.connected_ids[id] = callback

    def connect_to_type(self, type, callback):
        self.connected_types[type] = callback

    def connect_to_dbus(self, bus, path):
        remote_object = bus.get_object(path, "/Queue")
        queueinterface = dbus.Interface(remote_object, path)

        queueinterface.connect_to_signal("message_received", self.dispatch)

    def dispatch(self, local_id, response_to):
        print_color("dispatching: %d %d" % (local_id, response_to), 'grey')
        data = self.queue.peek(local_id)
        try:
            msg = Message.unpack(data, self.db)
        except Exception, e:
            print "Couldn't unpack", data
            return
        type = msg.type
        # execute the callbacks
        if self.connected_ids.has_key(response_to):
            print "execute on id", type
            callback = self.connected_ids[response_to]
            result = callback(msg)
            if result:
                self.queue.mark_as_processed(local_id)
            else:
                self.queue.mark_as_failed(local_id)
            return
        if self.connected_types.has_key(type):
            print "execute on type", type
            callback = self.connected_types[type]
            result = callback(msg)
            if result:
                self.queue.mark_as_processed(local_id)
            else:
                self.queue.mark_as_failed(local_id)
            return
        self.queue.mark_as_failed(local_id)

    def process_items(self):
        print "processing"
        session = self.db._Session()
        query = session.query(NetworkInQueueItem).filter_by(processed=0)
        for item in query:
            self.dispatch(item.id, 0)
        session.close()
