import gobject
from shared.data import Message, MessageType, UnitData, MissionData, Alarm, ActionType, Database

class TextMessageHandler(gobject.GObject):
    database = None
    queue = None
    controller = None

    def __init__(self, database, queue):
        gobject.GObject.__init__(self)
        self.database = database
        self.queue = queue

    def handle(self, message):
        print "handles mapobject", message
        subtype = message.subtype
        object = message.unpacked_data
        Database.add(self.database, object)
        self.emit("got-new-message")
        return True
    
gobject.type_register(TextMessageHandler)
gobject.signal_new("got-new-message", TextMessageHandler, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())