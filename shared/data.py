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

class EventType(object):
    '''
    Enumeration of all event types.
    '''
    add, change, remove = range(3)

# UNFINIISHED
class Event(Packable):
    def __init__(self, object, object_id = None, type = EventType.add, timestamp = datetime.now()):
        self.object = object
        self.object_id = object_id
        self.type = type
        self.timestamp = timestamp

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__.encode("utf-8"), 
                                         self.type, self.object_id,
                                         self.object, self.timestamp)

class MessageType(object):
    (mission, map, text, alarm, control, low_battery, status_update, mission_response, 
    journal_request, journal_confirmationresponse, journal_confirmationrequest, 
    journal_transfer, alarm_ack, vvoip_request, vvoip_response) = range(15)

class Message(object):
    '''
    All messages must be instances of this class.
    Enables packing and unpacking of raw messages.
    '''
    # The type of this message
    type = None
    # The priority of this message (lowest 0 - 9 highest)
    prio = 0
    # The packed data (json dumps) to send (a dict containing all variables)
    packed_data = None
    # The event
    unpacked_data = None
    
    timestamp = None
    
    def __init__(self, type = None, unpacked_data = None):
        '''
        Create a message.
        @param type:
        @param unpacked_data:
        '''
        self.type = type
        self.unpacked_data = unpacked_data
        self.timestamp = datetime.now()
#        if unpacked_data != None:
#            self.packed_data = unpacked_data.to_dict()
    
    def pack(self):
        '''
        Pack this message to a simplejson string.
        '''
        dict = {}
        dict["type"] = self.type
        dict["prio"] = self.prio
        dict["packed_data"] = self.unpacked_data.to_dict()
        dict["timestamp"] = self.timestamp.strftime("%s")
        return json.dumps(dict)

    def unpack(self, raw_message):
        '''
        Unpack a simplejson string to an object.
        @param raw_message: the simplejson string
        '''
        dict = json.loads(raw_message)
        self.type = dict["type"]
        self.prio = dict["prio"]
        self.timestamp = datetime.fromtimestamp(float(dict["timestamp"]))
        self.packed_data = dict["packed_data"]
        
        def create(dict):
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

        def create_mission(dict):
            # remove added class keys (and values)
            del dict["class"]
            # create the poi from its dict
            dict["poi"] = create(dict["poi"])
            
            # create the mission data object
            return MissionData(**dict)
        
        if self.type == MessageType.mission:
            # create the event object from the event object dict
            self.packed_data["object"] = create_mission(self.packed_data["object"])
            # create the event from the data
            event = create(self.packed_data)
            # set and return the message event
            self.unpacked_data = event
            
        elif self.type == MessageType.map:
            # create the event object from the event object dict
            self.packed_data["object"] = create(self.packed_data["object"])
            # create the event from the data
            event = create(self.packed_data)
            # set and return the message event
            self.unpacked_data = event

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
    
    event = Event(object = poi_data)
    
    m = Message(type = MessageType.map, unpacked_data = event)
    raw = m.pack()
    m = Message()
    m.unpack(raw)
    print "unpacked", m.unpacked_data, m.type, m.prio
