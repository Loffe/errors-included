from shared.data import Message, MessageType, UnitData, MissionData, Alarm, ActionType, Database

class TextMessageHandler(object):
    database = None
    queue = None
    controller = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def handle(self, message):
        print "handles mapobject", message
        subtype = message.subtype
        object = message.unpacked_data
        Database.add(self.database, object)
        return True