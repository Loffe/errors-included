from shared.data import Database, Message, MessageType, ActionType, IDType, ObjectID, TextMessage, JournalType, JournalRequest, JournalResponse
import config
import gobject

class ClientDatabase(Database):
    ''' Handles database querys and syncronizes with server '''
    queue = None

    def __init__(self, queue):
        Database.__init__(self)
        self.queue = queue
        self.dispatcher = None
        self.name = config.client.name
        self.id_stop = ObjectID(u"id_stop", None)
        self.id_start = ObjectID(u"id_start", None)
        self.id_current = ObjectID(u"id_current", None)
        self.id_nextstart = ObjectID(u"id_nextstart", None)
        self.id_nextstop = ObjectID(u"id_nextstop", None)
        self.get_ids()
        self.requested = False

    def add(self, object):
        # @TODO: decide order of local commit, network commit and signal emit
        session = self._Session()
        session.add(object)
        # if no id has been assigned to this object; DO IT!
        if object.id == None:
            # all medic ids should end with 3
            object.id = (self.id_current.value*10)+3
            self.id_current.value += 1

            # current id is large enough to request a new id range
            interval_mid = self.id_start.value + \
                           (self.id_stop.value - self.id_start.value)/2
            if (self.id_current.value > interval_mid  and not self.requested):
                self.request_ids()

            # if out of range, activate the next range
            elif self.id_current.value >= self.id_stop.value:
                self.id_current.value = self.id_nextstart.value
                self.id_nextstart.value = None
                self.id_stop.value = self.id_nextstop.value
                self.id_nextstop.value = None
                self.requested = False

            # save all ids to database
            self.save_ids()
        
        # save object to database
        session.commit()
        session.close()
        
        # enqueue a message with the added object
        if object.__class__ == TextMessage:
            msg = Message(self.name, "server", MessageType.text,
                          unpacked_data=object)
        elif object.__class__ == JournalRequest:
            msg = Message(self.name, "server", MessageType.journal, JournalType.request,
                          unpacked_data = object)
        elif object.__class__ == JournalResponse:
            msg = Message(self.name, "server", MessageType.journal, JournalType.response,
                          unpacked_data = object)
        else:
            msg = Message(self.name, "server", MessageType.object, ActionType.add,
                          unpacked_data=object)

        self.queue.enqueue(msg.packed_data, msg.prio)
        self.emit("mapobject-added", object)

    def change(self, object):
        Database.change(self, object)
        msg = Message(self.name, "server", MessageType.object, ActionType.change,
                      unpacked_data=object)
        self.queue.enqueue(msg.packed_data, msg.prio)

    def delete(self, object):
        Database.delete(self, object)
        msg = Message(self.name, "server", MessageType.object, ActionType.delete,
                      unpacked_data=object)
        self.queue.enqueue(msg.packed_data, msg.prio)

    def request_ids(self):
        '''
        Request a new range of ids from server.
        '''
        msg = Message(self.name, "server", MessageType.id, IDType.request,
                      unpacked_data=None)
        self.queue.enqueue(msg.packed_data, msg.prio)
        self.dispatcher.connect_to_type(MessageType.id, self.set_ids)
        self.requested = True
        print "requesting ids"
        
    def set_ids(self, msg):
        '''
        Set next range of ids (callback method used by dispatcher).
        @param msg: the message with recieved ids (from server).
        '''
        print "set id"
        data = msg.unpacked_data
        self.id_nextstart.value = data["nextstart"]
        self.id_nextstop.value = data["nextstop"]
        if self.id_current.value == None:
            self.id_current.value = self.id_nextstart.value
            self.id_start.value = self.id_nextstart.value
            self.id_nextstart.value = None
            self.id_stop.value = self.id_nextstop.value
            self.id_nextstop.value = None
        self.save_ids()
        self.emit("ready")
        
    def save_ids(self):
        '''
        Save all ids to database.
        '''
        session = self._Session()
        session.add(self.id_current)
        session.add(self.id_start)
        session.add(self.id_stop)
        session.add(self.id_nextstart)
        session.add(self.id_nextstop)
        session.commit()
        session.close()
        
    def get_ids(self):
        '''
        Get the ObjectID items from database. If saved; set them, else do nothing.
        '''
        session = self._Session()

        current = session.query(ObjectID).filter_by(name=u"id_current").first()
        if current != None:
            self.id_current = current

        start = session.query(ObjectID).filter_by(name=u"id_start").first()
        if start != None:
            self.id_start = start

        stop = session.query(ObjectID).filter_by(name=u"id_stop").first()
        if stop != None:
            self.id_stop = stop

        nextstart = session.query(ObjectID).filter_by(name=u"id_nextstart").first()
        if nextstart != None:
            self.id_nextstart = nextstart

        nextstop = session.query(ObjectID).filter_by(name=u"id_nextstop").first()
        if nextstop != None:
            self.id_nextstop = nextstop

        session.close()

    def ensure_ids(self):
        '''
        Ensure database has a range of ids to be able to add objects. 
        '''
        if self.id_current.value == None:
            self.request_ids()
        else:
            self.emit("ready")
