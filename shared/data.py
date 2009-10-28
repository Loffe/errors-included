class UnitType(object):
    commander, ambulance, other = range(3)

class ObstacleType(object):
    tree, hippie_volkswagon, broken_nuclear_power_plant = range(3)

class POIType(object):
    accident, pasta_wagon = range(2)

class MapObjectData(object):
    coord = None
    name = None
    timestamp = None

    def __init__(self, coord, name, timestamp):
        self.coord = coord
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return "<%s: %s, %s, %s>" % (self.__class__.__name__, self.coord, self.name, self.timestamp)

class UnitData(MapObjectData):
    type = UnitType.ambulance

class ObstacleData(MapObjectData):
    type = ObstacleType.hippie_volkswagon

class POIData(MapObjectData):
    type = POIType.pasta_wagon

class MissionData(object):
    number_of_wounded = None
    POI = None
    event_type = None
    contact_person = None
    other = None

    def __init__(self, event_type, POI, number_of_wounded, contact_person, other):
        self.event_type = event_type
        self.POI = POI
        self.number_of_wounded = number_of_wounded
        self.contact_person = contact_person
        self.other = other
        
class Message(object):
    type = None
    data = None    
    
    def __init__(self, raw_msg = None):
        self.unpack(raw_msg)
    
    """ till JSON tror vi
    """
    def pack(self):
        pass
    
    def unpack(self, raw_msg):
        if raw_msg != None:
            #packa upp
            pass

if __name__ == "__main__":
    print MapObjectData((15.5726, 58.4035), 'MapObject', 0)
    print UnitData((15.5726, 58.4035), 'MapObject', 0)
    print ObstacleData((15.5726, 58.4035), 'MapObject', 0)
    print POIData((15.5726, 58.4035), 'MapObject', 0)
    print UnitType.commander
