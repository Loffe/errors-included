import shared.data
from shared.data import ActionType

class MapObjectHandler(object):
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def handle(self, message):
        print "handles mapobject", message
        subtype = message.subtype
        object = message.unpacked_data
        if subtype == ActionType.change:
            pass
        elif subtype == ActionType.add:
            self.database.add(object)
        elif subtype == ActionType.delete:
            pass
        else:
            raise Error("Invalid subtype")

