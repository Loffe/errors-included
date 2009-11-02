# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

class Database(object):
    '''
    A sqlite3 database using sqlalchemy.
    '''
    
    def __init__(self):
        '''
        Create database engine and session.
        '''
        self.engine = create_engine('sqlite:///database.db', echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

# Create a base class to extend in order to be able to save to the database. 
Base = declarative_base()

class UnitType(object):
    commander, ambulance, other = range(3)

class ObstacleType(object):
    tree, bridge, road, other = range(4)

class POIType(object):
    accident, pasta_wagon = range(2)

class MapObjectData(object):
    '''
    All objects visible on map have data objects extending this class.
    '''
    __tablename__ = 'MapObjectData'
    id = Column(Integer, primary_key=True)
    data_type = Column(Integer)
    __mapper_args__ = {"polymorphic_on": data_type} 
    
    coordx = Column(Float)
    coordy = Column(Float)
    name = Column(UnicodeText)
    timestamp = Column(DateTime)
    
    def get_coords(self):
        return (self.coordx, self.coordy)
    
    def set_coords(self, x, y):
        self.coordx = x
        self.coordy = y
    
    coords = property(get_coords, set_coords)

    def __init__(self, coord, name, timestamp):
        '''
        Constructor. Creates a map object.
        @param coord: The coordinates of this object.
        @param name: The name of this object.
        @param timestamp: The time this object was created.
        '''
        self.coords = coord
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__.encode("utf-8"), 
                                     self.coordx, self.coordy, self.name.encode("utf-8"), 
                                     self.timestamp)

class UnitData(MapObjectData):
    '''
    All units have data objects extending this class.
    '''
    __tablename__ = 'UnitData'
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'UnitData'}

    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = UnitType.ambulance):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type

class ObstacleData(MapObjectData):
    __tablename__ = 'ObstacleData'
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'ObstacleData'}
    
    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = ObstacleType.tree):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type

class POIData(MapObjectData):
    __tablename__ = 'POIData'
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'POIData'}
    
    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = POIType.pasta_wagon):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type

class MissionData(Base):
    __tablename__ = 'MissionData'
    id = Column(Integer, primary_key=True)
    
    number_of_wounded = Column(Integer)
    poi_id = Column(Integer, ForeignKey('POIData.id'))
    poi = relation(POIData)
    event_type = Column(UnicodeText)
    contact_person = Column(UnicodeText)
    other = Column(UnicodeText)

    def __init__(self, event_type, POI, number_of_wounded, contact_person, 
                 other):
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
    pass
