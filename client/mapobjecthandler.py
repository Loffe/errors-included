from shared.data import Message, MessageType, UnitData, MissionData, ActionType, Database

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
            # if a unit_data with my name was added, set it to mine
            if object.__class__ == UnitData:
                if self.controller is not None and object.name == self.controller.name:
                    self.controller.unit_data = object
            # if a mission with my unit_data was added, assign me to it (show it)
            if object.__class__ == MissionData:
                for unit in object.units:
                    if unit.id == self.controller.unit_data.id:
                        self.controller.add_mission(object)
        elif subtype == ActionType.delete:
            pass
        else:
            raise Error("Invalid subtype")

        return True
