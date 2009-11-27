import shared.data

class VoipHandler(object):
    INTERVAL = 1000
    next_interval_start = 1
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def handler(self, message):
        
        print "YAWTAPSFS"
#        start = self.next_interval_start
#        stop = start + self.INTERVAL - 1
#        self.next_interval_start = stop + 1
#        ack = shared.data.Message("server", message.sender,
#                type=shared.data.MessageType.id,
#                subtype=shared.data.IDType.response,
#                unpacked_data={'class': 'dict', 'nextstart': start, 'nextstop': stop})
#        self.queue.enqueue(message.sender, ack.packed_data, 9)
#        print "providing"
