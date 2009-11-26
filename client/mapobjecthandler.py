from shared.data import Message, MessageType, MissionData, ActionType

class MapObjectHandler(object):
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
        if subtype == ActionType.change:
            pass
        elif subtype == ActionType.add:
            session = self.database._Session()
            session.add(object)
            session.commit()
            session.close()
            if object.__class__ == MissionData:
                for unit in object.units:
                    if unit.id == self.controller.unit_data.id:
                        self.controller.add_mission(object)
            self.database.emit("mapobject-changed", object)
        elif subtype == ActionType.delete:
            pass
        else:
            raise Error("Invalid subtype")

