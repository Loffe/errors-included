import gobject
import dbus
import dbus.mainloop.glib

import threading
import shared.data
import shared.messagedispatcher
import shared.queueinterface

from idprovider import IDProvider
from mapobjecthandler import MapObjectHandler
from database import ServerDatabase
from shared.data import MessageType


class ServerManager(object):
    queue = None
    database = None
    idprovider = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.database = shared.data.create_database(ServerDatabase())
        bus = dbus.SessionBus()
        self.queue = shared.queueinterface.get_interface(bus, "included.errors.Server")
        self.idprovider = IDProvider(self.database, self.queue)
        self.mapobjecthandler = MapObjectHandler(self.database, self.queue)
        self.messagedispatcher = shared.messagedispatcher.MessageDispatcher(bus,
                self.database,
                path="included.errors.Server")

        self.messagedispatcher.connect_to_type(shared.data.MessageType.id, self.idprovider.provide)
        self.messagedispatcher.connect_to_type(MessageType.object, self.mapobjecthandler.handle)

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
        u = User(u"ragnar", u"prydlig frisyr")
        session.add(u)
        u = User(u"slanggurka", u"smakar som nors")
        session.add(u)

        for name in [u"Erik", u"Martin", u"Freddie", u"Linus", u"Emil", u"DT"]:
            u = User(name, name)
            session.add(u)

            unit = UnitData(0, 0, name, datetime.now())
            session.add(unit)

        # Create units
#        u = UnitData(13, 37, "RD1337", datetime.now())
#        session.add(u)

        session.commit()
    else:
        server = ServerManager()
        server.dbusloop()
