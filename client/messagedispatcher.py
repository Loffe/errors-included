import dbus


class MessageDispatcher(object):
    connections = {}
    def __init__(self, bus):
        self.connect_to_dbus(bus)

    def connect_to_id(self, id, callback):
        self.connections[id] = callback;

    def connect_to_dbus(self, bus):
        remote_object = bus.get_object("included.errors.Client", "/Queue")
        queueinterface = dbus.Interface(remote_object, "included.errors.Client")

        queueinterface.connect_to_signal("message_available", self.dispatch)

    def dispatch(self, local_id, response_to):
        print local_id, response_to
