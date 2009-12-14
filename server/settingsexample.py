"""
Don't touch and really don't commit changes. If you create new variables
in settings.py you must also add them here
"""
from config import Config

server = Config()
server.port = 50000
server.ssh = True
server.primary = True
server.database = 'mysql://eriel743:PoAQjf29f@localhost/eriel743'

primary = Config()
primary.ip = 'sysi-14'
primary.port = 50000
primary.heartbeatport= 1337
primary.heartbeatinterval= 5000
