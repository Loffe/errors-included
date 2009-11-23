from shared.data import Packable, Base
from sqlalchemy import *


class User(Base, Packable):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    password = Column(UnicodeText)
    ip = Column(UnicodeText)

    def __init__(self, username, password=None):
        self.name = username
        self.password = password
        
    def __repr__(self):
        repr = ("<%s: %s, %s, %s, %s>" % 
                (self.__class__.__name__, self.id, self.name, self.password, self.ip))
        try:
            return repr.encode('utf-8')
        except:
            return repr
        
