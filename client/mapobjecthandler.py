# coding: utf-8
from shared.data import Message, MessageType, UnitData, MissionData, Alarm, ActionType, Database
import gobject

class MapObjectHandler(gobject.GObject):
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
        if subtype == ActionType.change:
            Database.change(self.database, object)
            self.database.emit("mapobject-changed", object)
            # if my mission was changed, change my mission
            if object.__class__ == MissionData:                
                for unit in object.units:
                    if self.controller is not None:
                        if unit.id == self.controller.unit_data.id:
                            self.emit("got-new-mission")

        elif subtype == ActionType.add:
            Database.add(self.database, object)
            # if a unit_data with my name was added, set it to mine
            if object.__class__ == UnitData:
                if self.controller is not None and object.name == self.controller.name:
                    self.controller.unit_data = object
            # if a mission with my unit_data was added, assign me to it (show it)
            if object.__class__ == MissionData:
                print self.controller.unit_data.id        
                for unit in object.units:
                    print unit.id
                    if self.controller is not None:
                        if unit.id == self.controller.unit_data.id:
                            self.emit("got-new-mission")
                            
                            print "blinking?"

        elif subtype == ActionType.delete:
            Database.delete(self.database, object)
            self.database.emit("mapobject-deleted", object)
        else:
            raise Error("Invalid subtype")

        return True

gobject.type_register(MapObjectHandler)
gobject.signal_new("got-new-mission", MapObjectHandler, gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ())
