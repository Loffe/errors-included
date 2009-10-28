# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Database(object):
    
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

Base = declarative_base()
class MapObjectData(Base):
    __tablename__ = 'MapObjectData'

    id = Column(Integer, primary_key=True)
    coordx = Column(Integer)
    coordy = Column(Integer)
    name = Column(Text)
    timestamp = Column(Text)

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
    mod = MapObjectData((0,0), u"ää", "14:37")
    db.session.add(mod)
#    db.session.delete(db.session.query(MapObjectData).filter_by(name="ää").first())
    db.session.commit()
    for mod in db.session.query(MapObjectData):
        print mod.name
#    unitdata = UnitData((0,0), "unit", "00:00")
#    db.session.add(unitdata)
#    for mod in db.session.query(MapObjectData).order_by(MapObjectData.id):
#        print mod
#    print db.session.query(MapObjectData).filter_by(name="Waagh").first()
#    print q
#    mod.name = 'altered'
#    print db.session.dirty
#    db.session.commit()
#    print db.session.dirty