from shared.data import Database, Message, MessageType, ActionType, IDType

class ClientDatabase(Database):
    ''' Handles database querys and syncronizes with server '''
    queue = None

    def __init__(self, queue):
        Database.__init__(self)
        self.queue = queue
        self.dispatcher = None
        self.name = "Anonymous"

    def add(self, object):
        # @TODO: decide order of local commit, network commit and signal emit
        Database.add(self, object)
        msg = Message(self.name, "server", MessageType.action, ActionType.add,
                      unpacked_data=object)
        self.queue.enqueue(msg.packed_data, msg.prio)

    def change(self, object):
        Database.change(self, object)
        msg = Message(self.name, "server", MessageType.action, ActionType.change,
                      unpacked_data=object)
        self.queue.enqueue(msg.packed_data, msg.prio)

    def delete(self, object):
        Database.delete(self, object)
        msg = Message(self.name, "server", MessageType.action, ActionType.delete,
                      unpacked_data=object)
        self.queue.enqueue(msg.packed_data, msg.prio)

    def request_ids(self):
        msg = Message(self.name, "server", MessageType.id, IDType.request,
                      unpacked_data=None)
        self.queue.enqueue(msg.packed_data, msg.prio)
        self.dispatcher.connect_to_id(msg.message_id, self.set_ids)
        
    def set_ids(self, msg):
        data = msg.unpacked_data
        self.id_nextstart = data["id_nextstart"]
        self.id_nextstop = data["id_nextstop"] 
