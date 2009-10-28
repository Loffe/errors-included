# -*- coding: utf-8 -*-
import datetime
from sys import exit
from sqlalchemy import Column, Integer, Text, UnicodeText, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Database(object):
    
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

Base = declarative_base()
class MapObjectData(Base):
    __tablename__ = 'MapObjectData'

    id = Column(Integer, primary_key=True)
    coordx = Column(Integer)
    coordy = Column(Integer)
    name = Column(UnicodeText)
    timestamp = Column(DateTime)

    def __init__(self, coord, name, timestamp):
        self.coordx = coord[0]
        self.coordy = coord[1]
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__, self.coordx, self.coordy, self.name, self.timestamp)

#class UnitData(MapObjectData):
#    type = Column(String)

if __name__ == '__main__':
    db = Database()
    Base.metadata.create_all(db.engine)
    mod = MapObjectData((0,0), u"hej", datetime.datetime(2005, 7, 14, 12, 30))
    db.session.add(mod)
    crap = MapObjectData((1,1), u"åäö", datetime.datetime(2006, 7, 14, 12, 30))
    db.session.add(crap)
#    for instance in db.session.query(MapObjectData).filter_by(name="hej"):
#        db.session.delete(instance)
    db.session.commit()
    for mod in db.session.query(MapObjectData):
        print mod.name.encode("utf-8"), mod.timestamp

    db.session.close()

#    unitdata = UnitData((0,0), "unit", "00:00")
#    db.session.add(unitdata)
