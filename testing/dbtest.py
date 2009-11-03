# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, relation
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Database(object):
    
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

class UnitType(object):
    commander, ambulance, other = range(3)

class ObstacleType(object):
    tree, bridge, road, other = range(4)

class POIType(object):
    accident, pasta_wagon = range(2)

class MapObjectData(Base):
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
    
    def set_coords(self, c):
        self.coordx = c[0]
        self.coordy = c[1]
    
    coords = property(get_coords, set_coords)

    def __init__(self, coord, name, timestamp):
        self.name = name
        self.timestamp = timestamp
        # hur skriver man?
        self.coords = coord

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__.encode("utf-8"), 
                                     self.coordx, self.coordy, self.name.encode("utf-8"), 
                                     self.timestamp)

#class UnitData(MapObjectData):
#    __tablename__ = 'UnitData'
#    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
#    __mapper_args__ = {'polymorphic_identity': 'UnitData'}
#    
#    type = Column(Integer)
#
#class POIData(MapObjectData):
#    __tablename__ = 'POIData'
#    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
#    __mapper_args__ = {'polymorphic_identity': 'POIData'}
#    
#    type = Column(Integer)
#
#    def __init__(self, coord, name, timestamp, type = POIType.pasta_wagon):
#        MapObjectData.__init__(self, coord, name, timestamp)
#        self.type = type

class ObstacleData(MapObjectData):
    __tablename__ = 'ObstacleData'
    __mapper_args__ = {'polymorphic_identity': 'ObstacleData'}
    id = Column(None, ForeignKey('MapObjectData.id'), primary_key=True)
    
    type = Column(Integer)

    def __init__(self, coord, name, timestamp, type = ObstacleType.tree):
        MapObjectData.__init__(self, coord, name, timestamp)
        self.type = type
    
#class MissionData(Base):
#    __tablename__ = 'MissionData'
#    id = Column(Integer, primary_key=True)
#    
#    number_of_wounded = Column(Integer)
#    poi_id = Column(Integer, ForeignKey('POIData.id'))
#    poi = relation(POIData)
#    event_type = Column(UnicodeText)
#    contact_person = Column(UnicodeText)
#    other = Column(UnicodeText)
#
#    def __init__(self, event_type, poi, number_of_wounded, contact_person, other):
#        self.event_type = event_type
#        self.poi = poi
#        self.number_of_wounded = number_of_wounded
#        self.contact_person = contact_person
#        self.other = other

if __name__ == '__main__':
    db = Database()
    Base.metadata.create_all(db.engine)
#    mod = MapObjectData((0,0), u"hej", datetime(2005, 7, 14, 12, 30))
#    db.session.add(mod)
#    poi = POIData((13, 37), u"målet", datetime(2021, 7, 14, 12, 30))
#    mission = MissionData(u"olycka", poi, 7, u"Stort Ove arnesson", u"Aj aj aj")
#    db.session.add(mission)
    coord = (15.5726, 58.4050)
    name = u"hinder"
    timestamp = datetime(2009,11,3,9,9)

    data = ObstacleData(coord, name, timestamp)
    db.session.add(data)
#    crap = MapObjectData((1,1), u"åäö", datetime(2006, 7, 14, 12, 30))
#    db.session.add(crap)
#    unitdata = UnitData((0,0), u"unit", datetime(2009,11,02, 13,37))
#    db.session.add(unitdata)
#    for instance in db.session.query(MapObjectData).filter_by(name="hej"):
#        db.session.delete(instance)
    db.session.commit()
    print ""
    for data in db.session.query(ObstacleData):
        print data.coords
#        .name.encode("utf-8")

    db.session.close()
