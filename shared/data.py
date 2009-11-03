# -*- coding: utf-8 -*-
import simplejson as json
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

# Create a base class to extend in order to be able to save to the database. 
Base = declarative_base()

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
        
    def add(self, object):
        self.session.add(object)
        self.session.commit()
        
    def delete(self, object):
        self.session.delete(object)
        self.session.commit()

class UnitType(object):
    ambulance, commander, other = range(3)

class ObstacleType(object):
    # always sort in alphabetic order!!!
    bridge, other, road, tree = range(4)

class POIType(object):
    accident, pasta_wagon = range(2)

class MapObjectData(Base):
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
    
    def set_coords(self, coords):
        self.coordx = coords[0]
        self.coordy = coords[1]
    
    coords = property(get_coords, set_coords)

    def __init__(self, coord, name, timestamp):
        '''
        Constructor. Creates a map object.
        @param coord: The coordinates of this object.
        @param name: The name of this object.
        @param timestamp: The time this object was created.
        '''
        self.coords = coord
        self.name = u""+name
        self.timestamp = timestamp
        
    def to_dict(self):
        dict = {}
#        dict["coords"] = self.coords
        for var in self.__dict__.keys():
            if not var.startswith("_"):
                dict[var] = self.__dict__[var]
        return dict

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__.encode("utf-8"), 
                                     self.coordx, self.coordy, self.name.encode("utf-8"), 
                                     self.timestamp)

class UnitData(MapObjectData):
    '''
    All units have data objects of this class.
    '''
    __tablename__ = 'UnitData'
    __mapper_args__ = {'polymorphic_identity': 'UnitData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)

    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = UnitType.ambulance):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type

class ObstacleData(MapObjectData):
    '''
    All obstacles have data objects of this class.
    '''
    __tablename__ = 'ObstacleData'
    __mapper_args__ = {'polymorphic_identity': 'ObstacleData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = ObstacleType.tree):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type

class POIData(MapObjectData):
    '''
    All Points of Interest (POIs) have data objects of this class.
    '''
    __tablename__ = 'POIData'
    __mapper_args__ = {'polymorphic_identity': 'POIData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = POIType.pasta_wagon):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type

class MissionData(Base):
    '''
    All missions have data objects of this class. 
    '''
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
        self.event_type = u""+event_type
        self.poi = POI
        self.number_of_wounded = number_of_wounded
        self.contact_person = u""+contact_person
        self.other = u""+other
        
class Message(object):
    '''
    All messages must be instances of this class.
    Enables packing and unpacking of raw messages.
    '''
    # The data to send (a dict containing all variables)
    data = None
    
    def __init__(self, object = None, raw_message = None):
        '''
        Create a message.
        @param object:
        @param raw_message:
        '''
        if self.raw_message != None:
            self.unpack(raw_message)
        else:
            self.data = object.to_dict()
    
    def pack(self):
        return json.dumps(self.data)
    
    def unpack(self, raw_message = None):
        if raw_message != None:
            self.data = json.loads(raw_message)
            # convert temp to type and object

def create_database():
    db = Database()
    Base.metadata.create_all(db.engine)
    return db
