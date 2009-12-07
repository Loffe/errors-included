from shared.data import Message, MessageType, ActionType, UnitType, JournalType
from shared.util import print_color

class JournalHandler(object):
    database = None
    queue = None

    def __init__(self, database, queue):
        self.database = database
        self.queue = queue

    def handle(self, message):
        print "handles journalrequest", message
        for u in self.database.get_all_units():
            if u.type == UnitType.commander:
                print "Sending to", u.name
                msg = Message(message.sender, u.name, MessageType.journal,
                              JournalType.confirmation_request, message.id,
                              message.unpacked_data, message.prio)
                return True
        print_color("Found no commander", 'red')
        return False
#        subtype = message.subtype
#        object = message.unpacked_data
#        for u in message.unpacked_data.units:
#            msg = Message(u"server", u.name, MessageType.text,
#                      ActionType.add, unpacked_data=object)
#            self.queue.enqueue(u.name, msg.packed_data, msg.prio)
