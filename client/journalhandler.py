import gobject
from shared.data import Message, MessageType, UnitData, MissionData, Alarm, ActionType, Database, JournalType, JournalRequest

class JournalHandler(gobject.GObject):
    database = None
    queue = None
    controller = None

    def __init__(self, database, queue):
        gobject.GObject.__init__(self)
        self.database = database
        self.queue = queue

    def handle(self, message):
        if message.subtype == JournalType.request:
            print "got new journal request", message
            Database.add(self.database, message.unpacked_data)
            self.emit("got-new-journal-request")
            return True
        elif message.subtype == JournalType.response:
            print "got new journal response", message
            Database.add(self.database, message.unpacked_data)
            self.emit("got-new-journal-response")
            return True
    
gobject.type_register(JournalHandler)
gobject.signal_new("got-new-journal-request", JournalHandler, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
gobject.signal_new("got-new-journal-response", JournalHandler, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
