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
from textmessagehandler import TextMessageHandler

from database import ServerDatabase
from shared.data import Message,MessageType,ActionType


class ServerManager(object):
    queue = None
    database = None
    idprovider = None
    voiphandler = None
    textmessagehandler = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.database = shared.data.create_database(ServerDatabase())
        bus = dbus.SessionBus()
        self.queue = shared.queueinterface.get_interface(bus, "included.errors.Server")

        self.queue.connect_to_signal("user_login", self._user_login)
        self.idprovider = IDProvider(self.database, self.queue)

        self.voiphandler = VoipHandler(self.database, self.queue)

        self.mapobjecthandler = MapObjectHandler(self.database, self.queue)
        self.textmessagehandler = TextMessageHandler(self.database, self.queue)

        self.messagedispatcher = shared.messagedispatcher.MessageDispatcher(bus,
                self.database,
                path="included.errors.Server")

        self.messagedispatcher.connect_to_type(shared.data.MessageType.id, self.idprovider.provide)

        self.messagedispatcher.connect_to_type(shared.data.MessageType.voip, self.voiphandler.handle)
        self.messagedispatcher.connect_to_type(shared.data.MessageType.vvoip, self.voiphandler.handle)

        self.messagedispatcher.connect_to_type(shared.data.MessageType.text, self.textmessagehandler.handle)
        self.messagedispatcher.connect_to_type(MessageType.object, self.mapobjecthandler.handle)

    def _user_login(self, username):
        print "User %s logged in to queue" % username
        units = self.database.get_all_units()
        for unit in units:
            unit_msg = Message("server", username,
                               MessageType.object, ActionType.add,
                               unpacked_data=unit);
            # Send initial messages with high prio
            self.queue.enqueue(username, unit_msg.packed_data, 9)

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

        db = create_database(ServerDatabase())

        meta = shared.data.Base.metadata
        meta.drop_all(bind=db.engine)
        db = create_database(ServerDatabase())
        session = db._Session()

        # Create users
        i = 0
        for name in [u"Erik", u"Martin", u"Freddie", u"Linus", u"Emil", u"DT", u"Leader", u"Slave"]:
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
