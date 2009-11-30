from shared.data import *

class VoipHandler(object):
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def handle(self, message):
        
        print "YAWTAPSFS"
        msg = Message(message.sender, message.reciever,
                      message.type, message.subtype,
                      unpacked_data=message.unpacked_data)
        self.queue.enqueue(msg.reciever, msg.packed_data, msg.prio)
        print "forwarding", msg

