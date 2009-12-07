import gobject
from shared.data import Message, MessageType, UnitData, MissionData, Alarm, ActionType, Database, JournalType

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
            self.emit("got-new-journal-request", message.unpacked_data)
            return True
    
gobject.type_register(JournalHandler)
gobject.signal_new("got-new-journal-request", JournalHandler, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))