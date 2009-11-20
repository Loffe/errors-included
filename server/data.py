from shared.data import Packable, Base
from sqlalchemy import *


class User(Base, Packable):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    name = Column(UnicodeText)
    password = Column(UnicodeText)

    def __init__(self, username, password=None):
        self.name = username
        self.password = password
