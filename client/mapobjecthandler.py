from shared.data import Message, MessageType, MissionData, ActionType, Database

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
            Database.change(self.database, object)
            self.database.emit("mapobject-changed", object)

        elif subtype == ActionType.add:
            Database.add(self.database, object)
            if object.__class__ == MissionData:
                for unit in object.units:
                    if unit.id == self.controller.unit_data.id:
                        self.controller.add_mission(object)
        elif subtype == ActionType.delete:
            pass
        else:
            raise Error("Invalid subtype")

