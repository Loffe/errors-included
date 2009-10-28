#from sqlalchemy import *
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Database(object):
    
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db', echo=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        mod = MapObjectData((2,4), "Waagh", "13:37")
        self.session.add(mod)
        

Base = declarative_base()
class MapObjectData(Base):
    __tablename__ = 'MapObjectData'

    id = Column(Integer, primary_key=True)
    coordx = Column(Integer)
    coordy = Column(Integer)
    name = Column(String)
    timestamp = Column(String)

    def __init__(self, coord, name, timestamp):
        self.coordx = coord[0]
        self.coordy = coord[1]
        self.name = name
        self.timestamp = timestamp

    def __repr__(self):
        return "<%s: %s, %s, %s, %s>" % (self.__class__.__name__, self.coordx, self.coordy, self.name, self.timestamp)

if __name__ == '__main__':
    db = Database()
    Base.metadata.create_all(db.engine)
    mod = db.session.query(MapObjectData).filter_by(name="Waagh").first()
    print mod
    mod.name = 'altered'
    print db.session.dirty
    db.session.commit()
    print db.session.dirty