"""
Don't touch and really don't commit changes. If you create new variables
in settings.py you must also add them here
"""
from config import Config

server = Config()
server.ip = '127.0.0.1'
server.port = 50000
server.localport = 50001
server.ssh = False
