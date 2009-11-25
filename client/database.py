from shared.data import Database, Message, MessageType, ActionType, IDType, ObjectID
import gobject

class ClientDatabase(Database):
    ''' Handles database querys and syncronizes with server '''
    queue = None

    def __init__(self, queue):
        Database.__init__(self)
        self.queue = queue
        self.dispatcher = None
        self.name = "Anonymous"
        self.id_stop = ObjectID(u"id_stop", None)
        self.id_current = ObjectID(u"id_current", None)
        self.id_nextstart = ObjectID(u"id_nextstart", None)
        self.id_nextstop = ObjectID(u"id_nextstop", None)
        self.get_ids()

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
        msg = Message("ragnar", "server", MessageType.id, IDType.request,
                      unpacked_data=None)
        self.queue.enqueue(msg.packed_data, msg.prio)
        self.dispatcher.connect_to_type(MessageType.id, self.set_ids)
        print "requesting ids"
        
    def set_ids(self, msg):
        print "set id"
        data = msg.unpacked_data
        self.id_nextstart.value = data["nextstart"]
        self.id_nextstop.value = data["nextstop"]
        if self.id_current.value == None:
            self.id_current.value = self.id_nextstart.value
            self.id_nextstart.value = None
            self.id_stop.value = self.id_nextstop.value
            self.id_nextstop.value = None
        self.save_ids()
        self.emit("ready")

    def ensure_ids(self):
#        current = None
#        stop = None
#        nextstart = None
#        nextstop = None
#
#        try:
#            current = self.id_current.value
#        except:
#            pass
#        try:
#            stop = self.id_stop.value
#        except:
#            pass
#        try:
#            nextstart = self.id_nextstart.value
#        except:
#            pass
#        try:
#            nextstop = self.id_nextstop.value
#        except:
#            pass

#        if nextstart != None and nextstop != None:
#            self.id_nextstart.value = nextstart
#            self.id_nextstop.value = nextstop
#        if current == None or stop == None:
#            if self.id_nextstart.value != None and self.id_nextstop.value != None:
#                self.id_current.value = self.id_nextstart.value
#                self.id_stop.value = self.id_nextstop.value
#                self.save_ids()
#                self.emit("ready")
#            else:
#                self.request_ids()
#        else:
#            self.id_current.value = current
#            self.id_stop.value = stop
#            self.save_ids()
#            self.emit("ready")
        self.request_ids()
