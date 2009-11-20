from shared.data import Database, Message, MessageType, ActionType

class ClientDatabase(Database):
    ''' Handles database querys and syncronizes with server '''
    queue = None

    def __init__(self, queue):
        Database.__init__(self)
        self.queue = queue
        self.name = "Anonymous"

    def add(self, object):
        # @TODO: decide order of local commit, network commit and signal emit
        Database.add(self, object)
        print object.has_changed(self)
        msg = Message(self.name, "server", MessageType.action, ActionType.add,
                      unpacked_data=object)
        self.queue.enqueue(msg.packed_data, msg.prio)
