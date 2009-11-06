# -*- coding: utf-8 -*-
import simplejson as json
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

# Create a base class to extend in order to be able to save to the database. 
Base = declarative_base()

# Relation; Mission holding its units data
units_in_missions = Table('UnitsInMissions', Base.metadata,
                    Column('mission_id', Integer, ForeignKey('MissionData.id')),
                    Column('unit_id', Integer, ForeignKey('UnitData.id')))


class Packable(object):
    '''
    Extend this class to be able to pack/unpack a message containing it.
    '''

    def to_dict(self):
        dict = {}
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

    def get_all_units(self):
        list = []
        for u in self.session.query(UnitData):
            list.append(u)
        return list

    def get_units(self, unit_ids):
        list = []
        q = self.session.query(UnitData).filter(UnitData.id.in_(unit_ids))
        for u in q:
            list.append(u)
        return list

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
    __mapper_args__ = {'polymorphic_identity': 'MapObjectData', "polymorphic_on": data_type} 
    
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

    def __init__(self, coordx, coordy, name, timestamp, id):
        '''
        Constructor. Creates a map object.
        @param coord: The coordinates of this object.
        @param name: The name of this object.
        @param timestamp: The time this object was created.
        '''
        self.coordx = coordx
        self.coordy = coordy
        self.name = name
        self.timestamp = timestamp
        self.id = id

    def __repr__(self):
        repr = "<%s: x=%s, y=%s, %s, %s>" % (self.__class__.__name__,
                                     self.coordx, self.coordy, self.name,
                                     self.timestamp)
        try:
            return repr.encode('utf-8')
        except:
            return repr 

class UnitData(MapObjectData):
    '''
    All units have data objects of this class.
    '''
    __tablename__ = 'UnitData'
    __mapper_args__ = {'polymorphic_identity': 'UnitData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)

    type = Column(Integer)

    def __init__(self, coordx, coordy, name, timestamp, 
                 type = UnitType.ambulance, id = None):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp, id)
        self.type = type

class ObstacleData(MapObjectData):
    '''
    All obstacles have data objects of this class.
    '''
    __tablename__ = 'ObstacleData'
    __mapper_args__ = {'polymorphic_identity': 'ObstacleData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coordx, coordy, name, timestamp, 
                 type = ObstacleType.tree, id = None):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp, id)
        self.type = type

class POIData(MapObjectData):
    '''
    All Points of Interest (POIs) have data objects of this class.
    '''
    __tablename__ = 'POIData'
    __mapper_args__ = {'polymorphic_identity': 'POIData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coordx, coordy, name, timestamp, 
                 type = POIType.pasta_wagon, id = None):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp, id)
        self.type = type

class Alarm(Base, Packable):
    __tablename__ = 'Alarm'
    id = Column(Integer, primary_key = True)
    
    event = Column(UnicodeText)
    location_name = Column(UnicodeText)
    poi_id = Column(Integer, ForeignKey('POIData.id'))
    poi = relation(POIData)
    timestamp = Column(DateTime)
    contact_person = Column(UnicodeText)
    contact_number = Column(UnicodeText)
    other = Column(UnicodeText)

    def __init__(self, event, location_name, poi, contact_person, 
                 contact_number, timestamp = datetime.now(), other = u""):
        self.event = event
        self.location_name = location_name
        self.poi = poi
        self.timestamp = timestamp
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.other = other
        
    def __repr__(self):
        repr = ("<%s: %s, %s, %s, %s, %s, %s, %s, %s>" % 
                (self.__class__.__name__,self.poi.coordx, self.poi.coordy, 
                 self.event, self.location_name, self.timestamp, 
                 self.contact_person, self.contact_number, self.other))
        try:
            return repr.encode('utf-8')
        except:
            return repr

class MissionData(Base, Packable):
    '''
    All missions have data objects of this class. 
    '''
    __tablename__ = 'MissionData'
    id = Column(Integer, primary_key=True)
    
    units = relation('UnitData', secondary=units_in_missions)

    number_of_wounded = Column(Integer)
    poi_id = Column(Integer, ForeignKey('POIData.id'))
    poi = relation(POIData)
    event_type = Column(UnicodeText)
    contact_person = Column(UnicodeText)
    other = Column(UnicodeText)

    def __init__(self, event_type, poi, number_of_wounded, contact_person, 
                 other = u"", units = None):
        self.event_type = event_type
        self.poi = poi
        self.number_of_wounded = number_of_wounded
        self.contact_person = contact_person
        self.other = other
        self.units = units
        
    def add_unit(self, unit):
        self.units.append(unit)
        
    def add_units(self, units):
        for unit in units:
            self.add_unit(unit)
    
    def remove_unit(self, unit):
        self.units.remove(unit)
        
    def remove_units(self, units):
        for unit in units:
            self.remove_unit(unit)
    
    def __repr__(self):
        repr = ("<%s: %s, %s, %s, %s, %s>" % 
                (self.__class__.__name__, self.poi.coordx, self.poi.coordy, 
                 self.event_type, self.number_of_wounded, self.contact_person))
        try:
            return repr.encode('utf-8')
        except:
            return repr

class EventType(object):
    '''
    Enumeration of all event types.
    '''
    add, change, remove = range(3)

class Event(Base, Packable):
    '''
    An Event declares what to be done with a specified object. It's possible to 
    pack/unpack. This makes it possible to send it as a message.
    '''
    __tablename__ = "Events"
    id = Column(Integer, primary_key = True)
    object_id = Column(Integer)
    type = Column(Integer)
    timestamp = Column(DateTime)
    
    def __init__(self, object_id, type, timestamp = datetime.now()):
        '''
        Constructor. Creates an event.
        @param object_id: the global unique id of the object.
        @param type: the event type (add, change or remove) specifies what to be
        done with the object.
        @param timestamp: the timestamp of this event.
        '''
        self.object_id = object_id
        self.type = type
        self.timestamp = timestamp

    def __repr__(self):
        repr = ("<%s: type=%s, %s; obj_id=%s>" % 
                (self.__class__.__name__, self.type, self.timestamp, 
                 self.object_id))
        try:
            return repr.encode('utf-8')
        except:
            return repr


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
    # The unpacked data
    unpacked_data = None
    # The timestamp of this message
    timestamp = None
    
    def __init__(self, type = None, unpacked_data = None, packed_data = None):
        '''
        Constructor. Creates a message.
        @param type: the type of this message
        @param unpacked_data: the unpacked data to pack
        @param packed_data: the packed data to unpack
        '''
        self.type = type
        self.unpacked_data = unpacked_data
        self.packed_data = packed_data
        self.timestamp = datetime.now()
        
        # message created from unpacked data
        if unpacked_data:
            # pack the unpacked data
            self.pack()
        # message created from packed data
        elif packed_data:
            # unpack the packed data
            self.unpack(packed_data)
    
    def pack(self):
        '''
        Pack this message to a simplejson string.
        '''
        dict = {}
        dict["type"] = self.type
        dict["prio"] = self.prio
        dict["timestamp"] = self.timestamp.strftime("%s")
        try:
            dict["packed_data"] = self.unpacked_data.to_dict()
        except:
            dict["packed_data"] = self.unpacked_data
        self.packed_data = json.dumps(dict)
        return self.packed_data

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
        
        # it's data packed to a dict
        if type(self.packed_data) == type({}):

            def create(dict):
                '''
                Create an object from a specified dictionary.
                @param dict: the dictionary to use.
                '''
                # remove added class key (and value)
                classname = dict["class"]
                del dict["class"]
                try:
                    # replace timestamp string with a real datetime
                    dict["timestamp"] = datetime.fromtimestamp(float(dict["timestamp"]))
                except:
                    pass
                try:
                    # create the poi from its dict
                    dict["poi"] = create(dict["poi"])
                except:
                    pass
                # create and return an instance of the object
                return globals()[classname](**dict)

            # create and set data
            self.unpacked_data = create(self.packed_data)

        # it's a default type
        else:
            # the packed data behave as the unpacked data (no need to convert)
            self.unpacked_data = dict["packed_data"]
        return self.unpacked_data

    def __repr__(self):
        repr = ("<%s: prio=%s, type=%s, %s; packed=%s, unpacked=%s>" % 
                (self.__class__.__name__, self.prio, self.type, self.timestamp, 
                 self.packed_data, self.unpacked_data))
        try:
            return repr.encode('utf-8')
        except:
            return repr


def create_database():
    '''
    Create the database.
    '''
    db = Database()
    # create tables and columns
    Base.metadata.create_all(db.engine)
    return db

if __name__ == '__main__':
    db = create_database()
    poi_data = POIData(12,113, u"goal", datetime.now(), POIType.accident)
#    db.add(poi_data)
    unit_data = UnitData(1,1, u"enhet 1337", datetime.now(), UnitType.commander)
#    db.add(unit_data)
    mission_data = MissionData(u"accidänt", poi_data, 7, u"Me Messen", u"det gör jävligt ont i benet på den dära killen dårå", [unit_data])
#    print mission_data
#    alarm = Alarm("räv", "Linköping", poi_data, "Klasse", "11111")
    
    db.add(mission_data)
#    event = Event(object = alarm)
#    event = Event(poi_data.id, EventType.add)
#    print "ALARM:", alarm
#    print "POI:", poi_data.__dict__
#    print Message(type = MessageType.map, unpacked_data = mission_data)
#    print "packed:", m1
#    m2 = Message(packed_data = m1.packed_data)
#    print "unpacked:", m2
