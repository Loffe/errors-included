import dbus


class MessageDispatcher(object):
    connections = {}
    def __init__(self, bus):
        self.connect_to_dbus(bus)

    def connect_to_id(self, id, callback):
        self.connections[id] = callback;

    def connect_to_dbus(self, bus, path="included.errors.Client"):
        remote_object = bus.get_object(path, "/Queue")
        queueinterface = dbus.Interface(remote_object, path)

        queueinterface.connect_to_signal("message_available", self.dispatch)

    def dispatch(self, local_id, response_to):
        print local_id, response_to
