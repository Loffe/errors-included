import gobject
import dbus
import dbus.mainloop.glib

import threading
import shared.data
import shared.messagedispatcher
import shared.queueinterface

from idprovider import IDProvider

from voiphandler import VoipHandler

from mapobjecthandler import MapObjectHandler

from database import ServerDatabase
from shared.data import MessageType


class ServerManager(object):
    queue = None
    database = None
    idprovider = None
    voiphandler = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.database = shared.data.create_database(ServerDatabase())
        bus = dbus.SessionBus()
        self.queue = shared.queueinterface.get_interface(bus, "included.errors.Server")

        self.queue.connect_to_signal("user_login", self._user_login)
        self.idprovider = IDProvider(self.database, self.queue)

        self.voiphandler = VoipHandler(self.database, self.queue)

        self.mapobjecthandler = MapObjectHandler(self.database, self.queue)

        self.messagedispatcher = shared.messagedispatcher.MessageDispatcher(bus,
                self.database,
                path="included.errors.Server")

        self.messagedispatcher.connect_to_type(shared.data.MessageType.id, self.idprovider.provide)

        self.messagedispatcher.connect_to_type(shared.data.MessageType.voip, self.voiphandler.handle)
        self.messagedispatcher.connect_to_type(shared.data.MessageType.vvoip, self.voiphandler.handle)

        self.messagedispatcher.connect_to_type(MessageType.object, self.mapobjecthandler.handle)

    def _user_login(self, username):
        print "User %s logged in to queue" % username
        s = self.database._Session()
        unit = s.query(shared.data.UnitData).filter_by(name=username).first()
        if unit is None:
            print "There is no unit with name %s" % username
        else:
            you_are_msg = Message("server", username,
                                  MessageType.object, ActionType.add,
                                  unpacked_data=unit);
            self.queue.enqueue(username, you_are_msg.packed_data, you_are_msg.prio)
        s.close()

    def _message_available(self, packed_data):
        print "_message_available"
        packed_data = str(packed_data)
        msg = shared.data.Message.unpack(packed_data, self.database)
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
        i = 0
        for name in [u"Erik", u"Martin", u"Freddie", u"Linus", u"Emil", u"DT"]:
            u = User(name, name)
            session.add(u)

            unit = UnitData(0, 0, name, datetime.now())
            unit.id = i*10 + 3
            i+=1
            session.add(unit)

        # Create units
#        u = UnitData(13, 37, "RD1337", datetime.now())
#        session.add(u)

        session.commit()
    else:
        server = ServerManager()
        server.dbusloop()
