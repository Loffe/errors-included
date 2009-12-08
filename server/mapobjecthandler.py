from shared.data import Message, MessageType, MissionData, ActionType, POIData, UnitData, Alarm, TextMessage

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
            self.database.change(object)
            for u in self.database.get_all_users():
                if u.name != message.sender:
                    msg = Message(u"server", u.name, MessageType.object,
                                  ActionType.change, unpacked_data=object)
                    self.queue.enqueue(u.name, msg.packed_data, msg.prio)

        elif subtype == ActionType.add:
            self.database.add(object)
            for u in self.database.get_all_users():
                if u.name != message.sender:
                    msg = Message(u"server", u.name, MessageType.object,
                                  ActionType.add, unpacked_data=object)
                    self.queue.enqueue(u.name, msg.packed_data, msg.prio)

        elif subtype == ActionType.delete:
            self.database.delete(object)
            for u in self.database.get_all_users():
                if u.name != message.sender:
                    msg = Message(u"server", u.name, MessageType.object,
                                  ActionType.delete, unpacked_data=object)
                    self.queue.enqueue(u.name, msg.packed_data, msg.prio)

        else:
            raise Error("Invalid subtype")

        return True
