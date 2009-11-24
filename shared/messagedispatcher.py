import dbus


class MessageDispatcher(object):
    connections = {}
    def __init__(self, bus, path="included.errors.Client"):
        self.connect_to_dbus(bus, path)

    def connect_to_id(self, id, callback):
        self.connections[id] = callback;

    def connect_to_dbus(self, bus, path):
        remote_object = bus.get_object(path, "/Queue")
        queueinterface = dbus.Interface(remote_object, path)

        queueinterface.connect_to_signal("message_received", self.dispatch)

    def dispatch(self, local_id, response_to):
        print local_id, response_to
        if self.connections.has_key(response_to):
            # execute the callback
            self.connections[response_to]()
