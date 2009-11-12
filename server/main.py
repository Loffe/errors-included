import gobject
import dbus
import dbus.mainloop.glib

import threading
import shared.data


class ServerManager(object):
    queueinterface = None
    database = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        remote_object = bus.get_object("included.errors.Server", "/Queue")
        self.queueinterface = dbus.Interface(remote_object, "included.errors.Server")

        self.queueinterface.connect_to_signal("message_available", self._message_available)

    def _message_available(self, packed_data):
        print "_message_available"
        packed_data = str(packed_data)
        msg = shared.data.Message(None, None, packed_data = packed_data)
        print msg

    def dbusloop(self):
        self.mainloop = gobject.MainLoop()
        gobject.threads_init()

        print "Running server on dbus."
        while self.mainloop.is_running():
            try:
                self.mainloop.run()
            except KeyboardInterrupt:
                self.mainloop.quit()



if __name__ == "__main__":
    server = ServerManager()
    server.dbusloop()
