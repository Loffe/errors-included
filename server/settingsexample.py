"""
Don't touch and really don't commit changes. If you create new variables
in settings.py you must also add them here
"""
from config import Config

server = Config()
server.port = 50000
server.ssh = False
server.primary = True
server.database = 'mysql://eriel743:PoAQjf29f@localhost/eriel743'
