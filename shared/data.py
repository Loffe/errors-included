# -*- coding: utf-8 -*-
import simplejson as json
from datetime import datetime
import gobject
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation, scoped_session
from sqlalchemy.orm.collections import InstrumentedList 
from sqlalchemy.ext.declarative import declarative_base

# Create a base class to extend in order to be able to save to the database. 
Base = declarative_base()

# Relation; Mission holding its units data
units_in_missions = Table('UnitsInMissions', Base.metadata,
                    Column('mission_id', Integer, ForeignKey('MissionData.id')),
                    Column('unit_id', Integer, ForeignKey('UnitData.id')))

units_in_text = Table('UnitsInText', Base.metadata,
                    Column('textmessage_id', Integer, ForeignKey('TextMessage.id')),
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
                if not isinstance(v, Packable):
                    if type(v) == datetime:
                        dict[var] = v.strftime("%s")
                    elif type(v) == InstrumentedList:
                        list = []
                        for unit in v:
                            list.append(unit.id)
                        dict[var] = list
                    elif var == "poi_id":
                        pass
                    else:
                        dict[var] = v
                elif var == "poi":
                        if self.__dict__[var].id is None:
                            print "poi to replace with id has no id, add it to database first"
                        dict["poi"] = self.__dict__[var].id
        dict["class"] = self.__class__.__name__
        return dict


class Database(gobject.GObject):
    '''
    A sqlite3 database using sqlalchemy.
    '''

    def __init__(self, path='sqlite:///database.db'):
        '''
        Create database engine and session.
        '''
        gobject.GObject.__init__(self)
        self.engine = create_engine(path, echo=False)
        self._Session = scoped_session(sessionmaker(bind=self.engine))
        
    def add(self, object):
        '''
        Add a new object to the database.
        @param object: the object to add.
        '''
        session = self._Session()
        result = session.query(object.__class__).filter_by(id=object.id).first()
        if result is None:
            session.add(object)
        else:
            import traceback
            traceback.print_stack()
            print "This cannot happen even in an alternative reality"
            self.copy(object, result)
            
        session.commit()
        session.close()
        self.emit("mapobject-added", object)
        
    def change(self, object):
        '''
        Change an existing objects state in the database.
        @param object: the object that has changed.
        '''
        if object is None:
            import traceback
            traceback.print_stack()
            print "Stop being stupid!"
        session = self._Session()
        object.timestamp = datetime.now()
        result = session.query(object.__class__).filter_by(id=object.id).first()
        if result is None:
            session.add(object)
            import traceback
            traceback.print_stack()
            print "This cannot happen in reality"
        else:
            self.copy(object, result)

        session.commit()
        session.close()
        self.emit("mapobject-changed", object)
        
    def delete(self, object):
        '''
        Delete an object from the database.
        @param object: the object to delete.
        '''
        session = self._Session()
        result = session.query(object.__class__).filter_by(id=object.id).first()
        if result is not None:
            session.delete(result)
            session.commit()
        session.close()
        self.emit("mapobject-deleted", object)
        
    def copy(self, origin, target):
        session = self._Session()
        attrs = {}
        for k in origin.__dict__.keys():
            if not k.startswith("_"):
                attrs[k] = origin.__dict__[k]

        for key in attrs.keys():
            if key == "poi":
                # poi_id is already copied
                pass
            elif key == "units":
                session.execute("DELETE FROM UnitsInMissions WHERE mission_id = %d" % origin.id)
                for unit in attrs["units"]:
                    sql = "INSERT INTO UnitsInMissions (mission_id, unit_id) VALUES (%s, %s)" % (attrs["id"], unit.id)
                    session.execute(sql)
            else:
                setattr(target, key, attrs[key])
        session.commit()
        session.close()

    def get_all_alarms(self):
        session = self._Session()
        alarms = []
        for a in session.query(Alarm):
            # do lazy load (setup relations)
            a.poi
            alarms.append(a)
        session.close()
        return alarms
    
    def get_all_missions(self):
        session = self._Session()
        missions = []
        for m in session.query(MissionData):
            # do lazy load (setup relations)
            m.poi
            m.units
            missions.append(m)
        session.close()
        return missions
    
    def textmessages(self):
        session = self._Session()
        textmessages = []
        for t in session.query(TextMessage):
            textmessages.append(t)
            t.units
        session.close()
        return textmessages
    
    def get_journals(self):
        session = self._Session()
        list = []
        for j in session.query(JournalResponse):
            list.append(j)
        session.close()
        return list

    def get_journal_requests(self):
        session = self._Session()
        requests = []
        for request in session.query(JournalRequest):
            requests.append(request)
        session.close()
        return requests
#    
#    def patientjournalmessage(self):
#        session = self._Session()
#        patientjournalmessage = []
#        for t in session.query(PatientJournalMessage):
#            patientjournalmessage.append(t)
#            t.units
#        session.close()
#        return patientjournalmessage
    
        #oanvänd
    def get_all_outboxmessages(self):
        session = self._Session()
        textmessages = []
        for t in session.query(TextMessage):
            if config.client.id[-2] == textmessages.id[-2]:
                textmessages.append(t)
        session.close()
        return textmessages
        
        #if config.client.type == 'commander':
    
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
    
class ObjectID(Base):
    __tablename__ = 'ObjectID'
    id = Column(Integer, primary_key = True)
    name = Column(UnicodeText)
    value = Column(Integer)
    
    prio = -1
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __repr__(self):
        repr = "<%s: name=%s, value=%s>" % (self.__class__.__name__,
                                            self.name, self.value)
        try:
            return repr.encode('utf-8')
        except:
            return repr

class UnitType(object):
    ambulance = u"ambulance" # Regular unit
    army = u"army" # short for Swedish Armed Forces
    commander = u"commander" # Nana nana nana nana LEADER! leader..
    srsa = u"srsa" # Swedish Rescue Services Agency (SRSA)
    other = u"other"

class POIType(object):
    structure = u"structure"
    event = u"event"
    obstacle = u"obstacle"
    flag = u"flag" # Remove?

class POISubType(object):
    bridge = u"bridge"
    tree = u"tree"
    accident = u"accident"
    fire = u"fire"
    pasta_wagon = u"pasta_wagon"
    hospital = u"hospital"
    base = u"base"
    other = u"other"
    


class NetworkInQueueItem(Base):
    __tablename__ = 'InQueue'
    id = Column(Integer, primary_key=True)
    processed = Column(Integer) # 0: ¬ processed, 1: processed, 2: failed
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
    name = Column(UnicodeText)
    sent = Column(Boolean)
    acked = Column(Boolean)
    prio = Column(Integer)
    data = Column(UnicodeText)

    def __init__(self, name, data, prio):
        self.sent = False
        self.name = name
        self.acked = False
        self.data = data
        self.prio = prio

class MapObjectData(Base, Packable):
    '''
    All objects visible on map have data objects extending this class.
    '''
    __tablename__ = 'MapObjectData'
    id = Column(Integer, primary_key=True)
    _data_type = Column('_data_type', String(50))
    __mapper_args__ = {'polymorphic_identity': 'MapObjectData', "polymorphic_on": _data_type} 
    
    coordx = Column(Float)
    coordy = Column(Float)
    name = Column(UnicodeText)
    timestamp = Column(DateTime)
    
    prio = 5
    
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
gobject.signal_new("ready", Database, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
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

    type = Column(UnicodeText)
    
    prio = 1

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
    
    type = Column(UnicodeText)
    subtype = Column(UnicodeText)
    
    prio = 7

    def __init__(self, coordx, coordy, name, timestamp, 
                 type = POIType.obstacle, subtype = None, id = None):
        MapObjectData.__init__(self, coordx, coordy, name, timestamp, id)
        self.type = type
        self.subtype = subtype
        
class TextMessage(Base, Packable):
    __tablename__ = 'TextMessage'
    id = Column(Integer, primary_key = True)
    
    units = relation('UnitData', secondary=units_in_text)
    
    subject = Column(UnicodeText)
    message_content = Column(UnicodeText)
    timestamp = Column(DateTime)
    sender = Column(UnicodeText)
    
    prio = 5
    
    def __init__(self, subject, message_content, units, sender, timestamp = datetime.now(), id = None):
        self.subject = subject
        self.message_content = message_content
        self.timestamp = timestamp
        self.units = units
        self.id = id
        self.sender = sender
     
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
            
        repr = ("<%s: subject=%s; message=%s, from=%s, to=%s, timestamp=%s, id=%s>" % 
                (self.__class__.__name__, self.subject, self.message_content, self.sender, 
                 self.units, self.timestamp , self.id))
        try:
            return repr.encode('utf-8')
        except:
            return repr        
        
class JournalRequest(Base, Packable):
    __tablename__ = 'JournalRequest'
    id = Column(Integer, primary_key = True)
    why = Column(UnicodeText)
    ssn = Column(UnicodeText)
    sender = Column(UnicodeText)
    # @TODO: check prio in spec
    prio = 8
    
    def __init__(self, why, ssn, sender, id = None):
        self.why = why
        self.ssn = ssn
        self.sender = sender
        self.id = id
        
    def __repr__(self):
            
        repr = ("<%s: why_entry=%s; social_security_number=%s, from=%s, id=%s>" % 
                (self.__class__.__name__, self.why, self.ssn, self.sender, self.id))
        try:
            return repr.encode('utf-8')
        except:
            return repr

class JournalResponse(Base, Packable):
    __tablename__ = 'JournalResponse'
    id = Column(Integer, primary_key = True)
    response_to = Column(Integer)
    allowed = Column(Boolean)
    why = Column(UnicodeText)
    ssn = Column(UnicodeText)
    journal = Column(UnicodeText)

    def __init__(self, response_to, allowed, why, ssn, journal, id = None):
        self.response_to = response_to
        self.allowed = allowed
        self.why = why
        self.ssn = ssn
        self.journal = journal
        self.id = id

    def __repr__(self):
        repr = ("<%s: allowed=%s; ssn=%s, response_to=%s>" %
                (self.__class__.__name__, self.allowed, self.ssn, self.response_to))
        try:
            return repr.encode('utf-8')
        except:
            return repr

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
    
    prio = 8

    def __init__(self, event, location_name, poi, contact_person, 
                 contact_number, number_of_wounded, other, 
                 timestamp = datetime.now(), id = None):
        self.event = event
        self.location_name = location_name
        self.poi = poi
        self.timestamp = timestamp
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.other = other
        self.number_of_wounded = number_of_wounded
        self.id = id
        
    def __repr__(self):
        repr = ("<%s: %s, %s, %s, %s, %s, %s, %s, %s, %s>" % 
                (self.__class__.__name__,self.poi.coordx, self.poi.coordy, 
                 self.event, self.location_name, self.number_of_wounded, self.timestamp, 
                 self.contact_person, self.contact_number, self.other))
        try:
            return repr.encode('utf-8')
        except:
            return repr
        
class MissionStatus(object):
    done = u"done" # genomfört, avslutat
    active = u"active" # genomförs, under arbete,
    alarm = u"alarm" # just larmad, ej påbörjat
    aborted = u"aborted" # avbrutet 

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
    contact_number = Column(UnicodeText)
    timestamp = Column(DateTime)
    other = Column(UnicodeText)
    status = Column(UnicodeText)
    
    prio = 7

    def __init__(self, event_type, poi, number_of_wounded, contact_person, contact_number,
                 other, units, status, timestamp = datetime.now(), id = None):
        self.event_type = event_type
        self.poi = poi
        self.number_of_wounded = number_of_wounded
        self.contact_person = contact_person
        self.contact_number = contact_number
        self.other = other
        self.timestamp = timestamp
        self.units = units
        self.id = id
        self.status = status
        
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

    def get_units(self, db):
        '''
        Returns a list of all UnitData-objects.
        @param db: The database to get them from.
        '''
        list = []
        for u in units:
            session = db._Session()
            data = session.query(UnitData).filter_by(id = u).first()
            list.append(data)
        return list
    
    def __repr__(self):
        repr = ("<%s: %s, %s, %s, %s, %s>" % 
                (self.__class__.__name__, self.poi.coordx, self.poi.coordy, 
                 self.event_type, self.number_of_wounded, self.contact_person))
        try:
            return repr.encode('utf-8')
        except:
            return repr

class MessageType(object):
    object = u"object"
    voip = u"voip"
    vvoip = u"vvoip"
    login = u"login"
    journal = u"journal"
    ack = u"ack"
    text = u"text"
    id = u"id"
    service_level = "service_level"

    # @TODO: Remove?
    mission = "mission"
    map = "map"
    alarm = "alarm"
    control = "control"
    low_battery = "low_battery"
    status_update = "status_update"
    mission_response = "mission_response"
    alarm_ack = "alarm_ack"
    vvoip_request = "vvoip_request"
    vvoip_response = "vvoip_response"
    action = "action"

class ActionType(object):
    add = "add"
    change = "change"
    delete = "delete"
    
class VOIPType(object):
    request = u"request"
    response = u"response"

class VVOIPType(object):
    request = u"request"
    response = u"response"
    
class IDType(object):
    request = "request"
    response = "response"

class JournalType(object):
    request = "request"
    response = "response"

class Message(object):
    '''
    All messages must be instances of this class.
    Enables packing and unpacking of raw messages.
    '''
    # Message id is set when queue puts item in db
    message_id = None
    # The id of the message this one is a response to
    response_to = None

    receiver = None
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
    
    def __init__(self, sender, receiver, type = None, subtype = None, response_to = 0, unpacked_data = None, prio = -1):
        '''
        Constructor. Creates a message.
        @param type: the type of this message
        @param unpacked_data: the unpacked data to pack
        '''
        self.sender = sender
        self.receiver = receiver
        self.type = type
        self.subtype = subtype
        self.unpacked_data = unpacked_data
        self.timestamp = datetime.now()
        self.response_to = response_to
        if unpacked_data is not None and hasattr(unpacked_data, "prio"):
            self.prio = unpacked_data.prio
        if prio != -1:
            self.prio = prio

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
        dict["receiver"] = self.receiver
        dict["response_to"] = self.response_to
        if self.message_id is not None:
            dict["message_id"] = self.message_id
        try:
            dict["packed_data"] = self.unpacked_data.to_dict()
        except:
            dict["packed_data"] = self.unpacked_data
        self.packed_data = json.dumps(dict)
        return unicode(self.packed_data)

    def unpack(cls, raw_message, database=None):
        '''
        Unpack a simplejson string to an object.
        @param raw_message: the simplejson string
        @param database: a Database to reconnect FK:s to SA Objects
        '''
        # raw_message contains sender and receiver
        self = cls(None, None)
        try:
            dict = json.loads(raw_message)
            self.type = dict["type"]
            self.subtype = dict["subtype"]
            self.prio = dict["prio"]
            self.sender = dict["sender"]
            self.receiver = dict["receiver"]
            self.timestamp = datetime.fromtimestamp(float(dict["timestamp"]))
            self.packed_data = dict["packed_data"]
            self.response_to = dict.get("response_to", None)
            self.message_id = dict.get("message_id", None)

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
                    if "units" in dict.keys():
                        try:
                            assert database is not None
                            unit_ids = dict["units"]
                            units = []
                            s = database._Session()
                            for uid in unit_ids:
                                data = s.query(UnitData).filter_by(id=uid).first()
                                if data is None:
                                    print "No unit with specified id found in database, sync error!"
                                units.append(data)
                            s.commit()
                            s.close()
                            dict["units"] = units
                        except AssertionError:
                            print "No database to unpack units from"
                    if "poi" in dict.keys():
                        try:
                            assert database is not None
                            poi_id = dict["poi"]
                            s = database._Session()
                            poi = s.query(POIData).filter_by(id=poi_id).first()
                            if poi is None:
                                print "No poi with specified id found in database, sync error!"
                            dict["poi"] = poi
                            s.commit()
                            s.close()
                        except AssertionError:
                            print "No database to unpack poi from"
                    # create and return an instance of the object
                    if classname == "dict":
                        return dict
                    else:
                        try:
                            # ensure utf-8
                            encodeddict = {}
                            for k in dict.keys():
                                 encodeddict[k.encode('utf-8')] = dict[k]
                            return globals()[classname](**encodeddict)
                        except Exception, e:
                            print e
                            raise ValueError("Failed with class: %s, dict: %s"
                                    % (classname, str(encodeddict)))

                # create and set data
                self.unpacked_data = create(self.packed_data)

            # it's a default type
            else:
                # the packed data behave as the unpacked data (no need to convert)
                self.unpacked_data = dict["packed_data"]
            return self
        except KeyError, ke:
            error = ValueError("Not a valid Message. Missing any keys maybe?")
            error.orig_error = ke
            error.data = raw_message
            raise error

    unpack = classmethod(unpack)

    def __repr__(self):
        repr = ("<%s: sender=%s, receiver=%s, prio=%s,\n    type=%s, sub=%s, ts=%s;\n    packed=%s>" %
                (self.__class__.__name__, self.sender, self.receiver, self.prio,
                 self.type, self.subtype, self.timestamp, self.packed_data))
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
    poi_data = POIData(12,113, u"goal", datetime(2012,12,12), POIType.event, POISubType.accident)
    db.add(poi_data)
    unit_data = UnitData(1,1, u"Freddie", datetime(2012,12,12), UnitType.ambulance)
    db.add(unit_data)
    mission_data = MissionData(u"Olycka", poi_data, 7, u"Freddie", u"12345",
                 u"Inget annat", [unit_data])
    db.add(mission_data)
    message = Message("ragnar", "server", unpacked_data = mission_data)
    print message.packed_data
    Message.unpack(message.packed_data, db)
#    db.add(mission_data)
#    poi_data2 = POIData(122,333, u"goal", datetime(2013,10,10), POIType.obstacle, POISubType.tree)
#    db.add(poi_data2)
#    alarm = Alarm(u"räv", u"Linköping", poi_data, u"Klasse", u"11111", 7, u"nada")
#    db.add(alarm)
#    msg = Message("ragnar", "server", unpacked_data = alarm)
#    print Message.unpack(msg.packed_data, db)
#    alarm = db._Session().query(Alarm).filter_by(id=alarm.id).first()
#    alarm.poi = poi_data2
#    print alarm
#    db.add(alarm)

#    poi_data = POIData(12,113, u"goal", datetime(2012,12,12), POIType.obstacle, POISubType.tree)
#    s = db._Session()
#    poi = s.query(POIData).first()
#    poi.name = "bajs"
#    s.commit()
#    s.close()
##    print poi_data, poi_data.to_dict()
#    db.add(poi_data)

#    print db.get_all_missions()
##    print mission_data.to_changed_list(db)
#    
#    units = []
#    units.append(unit_data)
#    text = TextMessage("hej", "hej", units)
#    db.add(text)
#
##    print mission_data.to_changed_list(db)
#    alarm = Alarm(u"räv", u"Linköping", poi_data, u"Klasse", u"11111", 7, u"nada")
#    db.add(alarm)
#    msg = Message("ragnar", "server", MessageType.action, ActionType.add,
#                  unpacked_data=poi_data)
#    print msg.packed_data
#    print Message.unpack(msg.packed_data, db)

#    alarm.event = "kuk"
#    db.change(alarm)
