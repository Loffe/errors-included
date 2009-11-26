import dbus
from shared.dbqueue import DatabaseInQueue
from shared.data import Message


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
        print local_id, response_to
        data = self.queue.peek(local_id)
        print data
        msg = Message.unpack(data, self.db)
        type = msg.type
        # execute the callbacks
        if self.connected_ids.has_key(response_to):
            print "execute on id", type
            self.connected_ids[response_to](msg)
        if self.connected_types.has_key(type):
            print "execute on type", type
            self.connected_types[type](msg)
