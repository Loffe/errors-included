from shared.data import Message, MessageType, ActionType, UnitType, JournalType, JournalRequest
from shared.util import print_color

class JournalHandler(object):
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def handle(self, message):
        print "handles journalrequest", message
        self.database.add(message.unpacked_data)
        if message.subtype == JournalType.request:
            for u in self.database.get_all_units():
                if u.type == UnitType.commander:
                    print "Sending to", u.name
                    msg = Message(message.sender, u.name, MessageType.journal,
                                  JournalType.request,
                                  unpacked_data = message.unpacked_data, prio = message.prio)
                    self.queue.enqueue(u.name, msg.packed_data, msg.prio)
                    return True
            print_color("Found no commander", 'red')
        elif message.subtype == JournalType.response:
            session = self.database._Session()
            req = session.query(JournalRequest).filter_by(id=message.unpacked_data.response_to).first()
            receiver= req.sender
            session.close()
            msg = Message(message.sender, receiver, MessageType.journal,
                          JournalType.response,
                          unpacked_data = message.unpacked_data, prio = message.prio)
            print_color("forwarded response to %s %s" % (msg.reciever, msg.packed_data), 'green')
            self.queue.enqueue(msg.reciever, msg.packed_data, msg.prio)
            return True
        return False
