import gobject
import dbus
import dbus.mainloop.glib

import threading
import shared.data
import shared.messagedispatcher


class ServerManager(object):
    queueinterface = None
    database = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus = dbus.SessionBus()
        self.message_dispatcher = shared.messagedispatcher.MessageDispatcher(bus,
                path="included.errors.Server")

    def _message_available(self, packed_data):
        print "_message_available"
        packed_data = str(packed_data)
        msg = shared.data.Message.unpack(packed_data)
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
    import sys
    if "resetdb" in sys.argv:
        import os
        from shared.data import create_database, UnitData
        from data import User
        from datetime import datetime
        if os.path.exists("database.db"):
            os.remove("database.db")
        db = create_database()
        session = db._Session()

        # Create users
        u = User(u"Ragnar", u"prydlig frisyr")
        session.add(u)
        u = User(u"Slanggurka", u"smakar som nors")
        session.add(u)

        # Create units
        u = UnitData(13, 37, "RD1337", datetime.now())
        session.add(u)

        session.commit()
    else:
        server = ServerManager()
        server.dbusloop()
