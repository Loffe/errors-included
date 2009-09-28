
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
    pass

class ObstacleData(MapObjectData):
    pass

class POIData(MapObjectData):
    pass

if __name__ == "__main__":
    print MapObjectData((15.5726, 58.4035), 'MapObject', 0)
    print UnitData((15.5726, 58.4035), 'MapObject', 0)
    print ObstacleData((15.5726, 58.4035), 'MapObject', 0)
    print POIData((15.5726, 58.4035), 'MapObject', 0)
