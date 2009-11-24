from shared.data import Database, Message, MessageType, ActionType, IDType
import gobject

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
        self.id_nextstart = data["nextstart"]
        self.id_nextstop = data["nextstop"]
        self.emit("ready")

    def ensure_ids(self):
        session = self._Session()
        current = session.query(ObjectID).filter_by(name="id_current").first().value
        stop = session.query(ObjectID).filter_by(name="id_stop").first().value
        nextstart = session.query(ObjectID).filter_by(name="id_nextstart").first().value
        nextstop = session.query(ObjectID).filter_by(name="id_nextstop").first().value
        if nextstart != None and nextstop != None:
            self.id_nextstart.value = nextstart
            self.id_nextstop.value = nextstop
        if current == None or stop == None:
            if self.id_nextstart.value != None and self.id_nextstop.value != None:
                self.id_current.value = self.id_nextstart.value
                session.add(self.id_current.value)
                self.id_stop.value = self.id_nextstop.value
                session.add(self.id_stop)
                self.emit("ready")
            else:
                self.request_ids()
        else:
            self.id_current.value = current
            session.add(self.id_current)
            self.stop.value = stop
            session.add(self.id_stop)
            self.emit("ready")
        session.commit()
        session.close()

gobject.type_register(Database)
gobject.signal_new("ready", Database, gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ())
