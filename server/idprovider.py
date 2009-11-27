import shared.data

class IDProvider(object):
    INTERVAL = 1000
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def provide(self, message):
        print message
        session = self.database._Session()
        # Fetch next available id from db
        nextstart = session.query(shared.data.ObjectID).filter_by(name=u"id_nextstart").first()
        if nextstart is None:
            nextstart = shared.data.ObjectID(u"id_nextstart", 1000)

        start = nextstart.value
        stop = start + self.INTERVAL - 1

        # Update next available id
        nextstart.value = stop + 1
        session.add(nextstart)
        session.commit()
        session.close()
        ack = shared.data.Message("server", message.sender,
                type=shared.data.MessageType.id,
                subtype=shared.data.IDType.response,
                unpacked_data={'class': 'dict', 'nextstart': start, 'nextstop': stop})
        self.queue.enqueue(message.sender, ack.packed_data, 9)
        print "providing"
