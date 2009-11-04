# -*- coding: utf-8 -*-
import simplejson as json
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

# Create a base class to extend in order to be able to save to the database. 
Base = declarative_base()

class Packable(object):
    '''
    Extend this class to be able to pack/unpack a message containing it.
    '''
    def to_dict(self):
        dict = {}
#        dict["coords"] = self.coords
        for var in self.__dict__.keys():
            if not var.startswith("_"):
                v = self.__dict__[var]
                try:
                    dict[var] = self.__dict__[var].to_dict()
                except AttributeError:
                    if type(v) == datetime:
                        dict[var] = v.strftime("%s")
                    else:
                        dict[var] = v
        dict["class"] = self.__class__.__name__
        return dict

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

class MapObjectData(Base, Packable):
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

    def __init__(self, coordx, coordy, name, timestamp):
        '''
        Constructor. Creates a map object.
        @param coord: The coordinates of this object.
        @param name: The name of this object.
        @param timestamp: The time this object was created.
        '''
        self.coordx = coordx
        self.coordy = coordy
        self.name = u""+name
        self.timestamp = timestamp

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

    def __init__(self, coordx, coordy, name, timestamp, type = UnitType.ambulance):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp)
        self.type = type

class ObstacleData(MapObjectData):
    '''
    All obstacles have data objects of this class.
    '''
    __tablename__ = 'ObstacleData'
    __mapper_args__ = {'polymorphic_identity': 'ObstacleData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coordx, coordy, name, timestamp, type = ObstacleType.tree):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp)
        self.type = type

class POIData(MapObjectData):
    '''
    All Points of Interest (POIs) have data objects of this class.
    '''
    __tablename__ = 'POIData'
    __mapper_args__ = {'polymorphic_identity': 'POIData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coordx, coordy, name, timestamp, type = POIType.pasta_wagon):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp)
        self.type = type

class MissionData(Base, Packable):
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

    def __init__(self, event_type, poi, number_of_wounded, contact_person, 
                 other = ""):
        self.event_type = u""+event_type
        self.poi = poi
        self.number_of_wounded = number_of_wounded
        self.contact_person = u""+contact_person
        self.other = u""+other
    
    def __repr__(self):
        return "<%s: %s, %s, %s, %s, %s>" % (self.__class__.__name__.encode("utf-8"), 
                                     self.poi.coordx, self.poi.coordy, self.event_type, 
                                     self.number_of_wounded, self.contact_person)

# UNFINIISHED
class Event(Packable):
    def __init__(self, type, event, parameters, timestamp = datetime.now()):
        self.type = type
        self.event = event
        self.parameters = parameters
        self.timestamp = timestamp

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__.encode("utf-8"), 
                                         self.type, self.event.encode("utf-8"),
                                         self.parameters, self.timestamp)

class Message(object):
    '''
    All messages must be instances of this class.
    Enables packing and unpacking of raw messages.
    '''
    # The data to send (a dict containing all variables)
    data = None
    object = None
    
    def __init__(self, object = None):
        '''
        Create a message.
        @param object: the object to use as message.
        '''
        if object != None:
            self.data = object.to_dict()
    
    def pack(self):
        '''
        Pack this message to a simplejson string.
        '''
        return json.dumps(self.data)

    def unpack(self, raw_message):
        '''
        Unpack a simplejson string to an object.
        @param raw_message: the simplejson string
        '''
        self.data = json.loads(raw_message)
        data_class = self.data["class"]
        object = None
        
        def create_map_object_data(dict):
            '''
            Create a POIData object from a specified dictionary.
            @param dict: the dictionary to use.
            '''
            # remove added class key (and value)
            classname = dict["class"]
            del dict["class"]
            # replace timestamp string with a real datetime
            dict["timestamp"] = datetime.fromtimestamp(float(dict["timestamp"]))
            return globals()[classname](**dict)
        
        # Class MissionData
        if data_class == "MissionData":
            # remove added class keys (and values)
            del self.data["class"]
            
            # create the poi from its dict
            self.data["poi"] = create_map_object_data(self.data["poi"])
            
            # create the mission data object
            object = MissionData(**self.data)

        # Class extends MapObjectData
        else:
            object = create_map_object_data(self.data)
            
        # set and return the message object
        self.object = object
        return object

def create_database():
    '''
    Create the database.
    '''
    db = Database()
    Base.metadata.create_all(db.engine)
    return db

if __name__ == '__main__':
    poi_data = POIData(12,113, "goal", datetime.now(), POIType.accident)
    mission_data = MissionData("accident", poi_data, 7, "Me Messon", "")
    m = Message(object = mission_data)
    raw = m.pack()
    print "messsage_data", type(m.data), m.data
    print "raw", type(raw), raw
    m = Message()
    m.unpack(raw)
    print "unpacked", m.object
