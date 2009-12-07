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

server.backup = Config()
server.backup.ip = 'localhost'
server.backup.port = 60000

queue = Config()
queue.reconnect_interval = 10*1000

client = Config()
client.name = u'Anonymous'
client.password = u'Anonymous'
client.type = u'ambulance'
client.id = -1

