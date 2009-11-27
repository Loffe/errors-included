from shared.data import *

class VoipHandler(object):
    INTERVAL = 1000
    next_interval_start = 1
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def voip_handler(self, message):
        print "waagh"
#        sender = message.sender
#        reciever = message.reciever
#        type = message.type
#        subtype = message.subtype
#        data = message.unpacked_data
#        
#        msg = Message(sender, reciever, type, subtype)
#        
#        if subtype == VOIPType.request:
#            data = message.unpacked_data
#            ip = data.ip
#            port = data.port
#            
#    
#            msg = shared.data.Message("server", reciever,
#                                      type=shared.data.MessageType.voip, 
#                                      subtype=shared.data.VOIPType.request,
#                                      unpacked_data={"ip": ip, "port": port,
#                                                     "class": "dict"})
#            self.queue.enqueue(msg.packed_data, msg.prio)
#        elif subtype == VOIPType.response:
#            data = message.unpacked_data
#            ip = data.ip
#            port = data.port
#            
#    
#            msg = shared.data.Message("server", reciever,
#                                      type=shared.data.MessageType.voip, 
#                                      subtype=shared.data.VOIPType.request,
#                                      unpacked_data={"ip": ip, "port": port,
#                                                     "class": "dict"})
#            self.queue.enqueue(msg.packed_data, msg.prio)

    def vvoip_handler(self, message):
        pass
