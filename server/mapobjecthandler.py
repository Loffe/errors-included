from shared.data import Message, MessageType, MissionData, ActionType

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
            if object.__class__ == MissionData:
                for unit in object.units:
                    msg = Message(u"server", u"ragnar", MessageType.object, 
                                  ActionType.add, unpacked_data=object)
                    print "packed data, rdy to enqueue:", msg.packed_data
                    self.queue.enqueue(msg.reciever, msg.packed_data, msg.prio)
        elif subtype == ActionType.delete:
            pass
        else:
            raise Error("Invalid subtype")

