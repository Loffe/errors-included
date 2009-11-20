# -*- coding: utf-8 -*-
import simplejson as json
from datetime import datetime
import gobject
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation, scoped_session
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

    def to_list(self):
        '''
        Returns this object as a list representation of this object with
        encapsulated objects first and self as last element.
        '''
        list = []
        for var in self.__dict__.keys():
            v = self.__dict__[var]
            if isinstance(v, Packable):
                list.append(v.to_dict())
        list.append(self.to_dict())
        return list

    def to_dict(self):
        '''
        Returns this object as a dictionary representation (no encapsulated 
        objects included, only their id)
        '''
        dict = {}
        for var in self.__dict__.keys():
            if not var.startswith("_"):
                v = self.__dict__[var]
                if not isinstance(self.__dict__[var], Packable):
#                    self.__dict__[var].to_dict()
#                except AttributeError:
                    if type(v) == datetime:
                        dict[var] = v.strftime("%s")
                    else:
                        dict[var] = v
        dict["class"] = self.__class__.__name__
        return dict
    
    def has_changed(self, database):
        '''
        Check if this objects state is different than the state of this object 
        in the database.
        '''
        session = database._Session()
        state_in_db = session.query(self.__class__).filter_by(id=self.id).first()
        session.close()
        print state_in_db, "vs.", self
        if state_in_db != None:
            if state_in_db.timestamp == self.timestamp:
                return False 
        return True
        
    def to_changed_list(self):
        '''
        Returns a list representation of this object containing only the 
        encapsulated objects that has changed.
        '''
        list = []
        for var in self.__dict__.keys():
            v = self.__dict__[var]
            if isinstance(v, Packable):
                if v.has_changed():
                    list.append(v.to_dict())
        list.append(self.to_dict())
        return list

class Database(gobject.GObject):
    '''
    A sqlite3 database using sqlalchemy.
    '''

    def __init__(self):
        '''
        Create database engine and session.
        '''
        gobject.GObject.__init__(self)
        self.engine = create_engine('sqlite:///database.db', echo=False)
        self._Session = scoped_session(sessionmaker(bind=self.engine))
#        self.session = self._Session()
        
    def add(self, object):
        '''
        Add a new object to the database.
        @param object: the object to add.
        '''
        session = self._Session()
        session.add(object)
        session.commit()
        session.close()
        self.emit("mapobject-added", object)
        
    def change(self, object):
        '''
        Change an existing objects state in the database.
        @param object: the object that has changed.
        '''
        session = self._Session()
        object.timestamp = datetime.now()
        session.add(object)
        session.commit()
        session.close()
        self.emit("mapobject-changed", object)
        
    def delete(self, object):
        '''
        Delete an object from the database.
        @param object: the object to delete.
        '''
        session = self._Session()
        session.delete(object)
        session.commit()
        session.close()
        self.emit("mapobject-deleted", object)
        
    def get_all_alarms(self):
        session = self._Session()
        alarms = []
        for a in session.query(Alarm):
            for p in session.query(POIData).filter_by(id=a.poi_id):
                a.poi = p
            alarms.append(a)
        session.close()
        return alarms

    def get_all_units(self):
        session = self._Session()
        list = []
        for u in session.query(UnitData):
            list.append(u)
        session.close()
        return list
    
    def get_all_mapobjects(self):
        session = self._Session()
        list = []
        for u in session.query(MapObjectData):
            list.append(u)
        session.close()
        return list

    def get_units(self, unit_ids):
        session = self._Session()
        list = []
        units = session.query(UnitData).filter(UnitData.id.in_(unit_ids))
        for u in units:
            list.append(u)
        session.close()
        return list

class UnitType(object):
    (ambulance, # Regular unit
     army, # short for Swedish Armed Forces
     commander, # Nana nana nana nana LEADER! leader..
     srsa, # Swedish Rescue Services Agency (SRSA) 
     other) = range(5)

class POIType(object):
    accident, fire, pasta_wagon, obstacle, flag = range(5)

class POISubType(object):
    tree, broken_brigde, broken_nuclear_power_plant = range(3)

class NetworkInQueueItem(Base):
    __tablename__ = 'InQueue'
    id = Column(Integer, primary_key=True)
    processed = Column(Boolean)
    data = Column(UnicodeText)
    def __init__(self, data, prio=0):
        ''' Construct a new queue item.
        
        prio is not used, it's only to have same __init__ interface as NetworkOutQueueItem
        '''
        self.data = data
        self.processed = False

class NetworkOutQueueItem(Base):
    __tablename__ = 'OutQueue'
    id = Column(Integer, primary_key=True)
    sent = Column(Boolean)
    acked = Column(Boolean)
    prio = Column(Integer)
    data = Column(UnicodeText)

    def __init__(self, data, prio):
        self.sent = False
        self.acked = False
        self.data = data
        self.prio = prio

class MapObjectData(Base, Packable):
    '''
    All objects visible on map have data objects extending this class.
    '''
    __tablename__ = 'MapObjectData'
    id = Column(Integer, primary_key=True)
    _data_type = Column(Integer)
    __mapper_args__ = {'polymorphic_identity': 'MapObjectData', "polymorphic_on": _data_type} 
    
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

gobject.type_register(Database)
gobject.signal_new("mapobject-added", Database, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
gobject.signal_new("mapobject-changed", Database, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
gobject.signal_new("mapobject-deleted", Database, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))

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

class POIData(MapObjectData):
    '''
    All Points of Interest (POIs) have data objects of this class.
    '''
    __tablename__ = 'POIData'
    __mapper_args__ = {'polymorphic_identity': 'POIData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)
    subtype = Column(Integer)

    def __init__(self, coordx, coordy, name, timestamp, 
                 type = POIType.pasta_wagon, subtype = None, id = None):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp, id)
        self.type = type
        self.subtype = subtype

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
    number_of_wounded = Column(Integer)

    def __init__(self, event, location_name, poi, contact_person, 
                 contact_number, number_of_wounded, other, timestamp = datetime.now()):
        self.event = event
        self.location_name = location_name
        self.poi = poi
        self.timestamp = timestamp
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.other = other
        self.number_of_wounded = number_of_wounded
        
    def __repr__(self):
        repr = ("<%s: %s, %s, %s, %s, %s, %s, %s, %s, %s>" % 
                (self.__class__.__name__,self.poi.coordx, self.poi.coordy, 
                 self.event, self.location_name, self.number_of_wounded, self.timestamp, 
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

class MessageType(object):
    (mission, map, text, alarm, control, low_battery, status_update, mission_response, 
    journal_request, journal_confirmationresponse, journal_confirmationrequest, 
    journal_transfer, alarm_ack, vvoip_request, vvoip_response, login, login_ack, action) = range(18)

class ActionType(object):
    add, update, remove = range(3)

class JournalType(object):
    request, confirmation_response, confirmation_request, transfer = range(4)

class Message(object):
    '''
    All messages must be instances of this class.
    Enables packing and unpacking of raw messages.
    '''
    message_id = None
    # The id of the message this one is a response to
    response_to = None

    reciever = None
    sender = None
    # The type of this message
    type = None
    subtype = None
    # The priority of this message (lowest 0 - 9 highest)
    prio = 0
    # The packed data (json dumps) to send (a dict containing all variables)
    packed_data = None
    # The unpacked data
    unpacked_data = None
    # The timestamp of this message
    timestamp = None
    
    def __init__(self, sender, reciever, type = None, subtype = None, response_to = 0, unpacked_data = None):
        '''
        Constructor. Creates a message.
        @param type: the type of this message
        @param unpacked_data: the unpacked data to pack
        '''
        self.sender = sender
        self.reciever = reciever
        self.type = type
        self.subtype = subtype
        self.unpacked_data = unpacked_data
        self.timestamp = datetime.now()
        self.response_to = response_to
        
        # pack the unpacked data
        self.pack()
    
    def pack(self):
        '''
        Pack this message to a simplejson string.
        '''
        dict = {}
        dict["type"] = self.type
        dict["subtype"] = self.subtype
        dict["prio"] = self.prio
        dict["timestamp"] = self.timestamp.strftime("%s")
        dict["sender"] = self.sender
        dict["reciever"] = self.reciever
        dict["response_to"] = self.response_to
        try:
            dict["packed_data"] = self.unpacked_data.to_dict()
        except:
            dict["packed_data"] = self.unpacked_data
        self.packed_data = json.dumps(dict)
        return self.packed_data

    def unpack(cls, raw_message):
        '''
        Unpack a simplejson string to an object.
        @param raw_message: the simplejson string
        '''
        # raw_message contains sender and reciever
        self = cls(None, None)
        try:
            dict = json.loads(raw_message)
            self.type = dict["type"]
            self.subtype = dict["subtype"]
            self.prio = dict["prio"]
            self.sender = dict["sender"]
            self.reciever = dict["reciever"]
            self.timestamp = datetime.fromtimestamp(float(dict["timestamp"]))
            self.packed_data = dict["packed_data"]
            self.response_to = dict["response_to"] if dict.has_key("response_to") else None

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
                    # create and return an instance of the object
                    if classname == "dict":
                        return dict
                    else:
                        try:
                            return globals()[classname](**dict)
                        except Exception, e:
                            raise ValueError("Failed with class: %s, dict: %s"
                                    % (classname, str(dict)))
                            print e

                # create and set data
                self.unpacked_data = create(self.packed_data)

            # it's a default type
            else:
                # the packed data behave as the unpacked data (no need to convert)
                self.unpacked_data = dict["packed_data"]
            return self
        except KeyError, ke:
            raise ValueError("Not a valid Message. Missing any keys maybe?")

    unpack = classmethod(unpack)

    def __repr__(self):
        repr = ("<%s: sender=%s, receiver=%s, prio=%s, type=%s, %s; packed=%s, unpacked=%s>" % 
                (self.__class__.__name__, self.sender, self.reciever, self.prio,
                 self.type, self.timestamp, self.packed_data, self.unpacked_data))
        try:
            return repr.encode('utf-8')
        except:
            return repr


def create_database(db = Database()):
    '''
    Create the database.
    '''

    # create tables and columns
    Base.metadata.create_all(db.engine)
    return db


if __name__ == '__main__':
    print "Testing db"
    db = create_database()

    poi_data = POIData(12,113, u"goal", datetime(2012,12,12), POIType.accident, POISubType.tree)
#    print poi_data, poi_data.to_dict()
#    db.add(poi_data)
#    unit_data = UnitData(1,1, u"enhet 1337", datetime.now(), UnitType.commander)
#    db.add(unit_data)
#    mission_data = MissionData(u"accidänt", poi_data, 7, u"Me Messen", u"det gör jävligt ont i benet på den dära killen dårå", [unit_data])
#    db.add(mission_data)
#    print mission_data
    alarm = Alarm("räv", "Linköping", poi_data, "Klasse", "11111", 7, "nada")
    db.add(alarm)

    alarm.event = "kuk"
    db.change(alarm)


