import gobject
import socket
import threading
import Queue

import shared.data
from shared.dbqueue import DatabaseInQueue, DatabaseOutQueue

from shared.util import getLogger
log = getLogger("nw-queue.log")

class NetworkQueue(gobject.GObject):
    queue = None
    socket = None

    def __init__(self, socket, databasequeue):
        self.__gobject_init__()
        self.socket = socket
        self.queue = databasequeue

    def replace_socket(self, socket):
        print self.__class__.__name__, "got a new socket"
        self.socket = socket

gobject.type_register(NetworkQueue)
gobject.signal_new("socket-broken", NetworkQueue, gobject.SIGNAL_RUN_FIRST,
                   gobject.TYPE_NONE, ())

class NetworkOutQueue(NetworkQueue):
    sending = False
    need_connection = True

    def __init__(self, socket, db):
        NetworkQueue.__init__(self, socket, DatabaseOutQueue(db))
        if self.socket:
            self.need_connection = False

    def enqueue(self, packed_data, prio):
        print "enqueued"
        local_id = self.queue.put(unicode(packed_data), prio)
        if not self.sending:
            self.start_sending()
        return local_id

    def start_sending(self):
        '''
        Starts a send burst in a new thread
        '''
        if self.need_connection:
            return
        print "starting send burst"
        self.sending = True
        threading.Thread(target=self.send_loop).start()

    def replace_socket(self, socket):
        NetworkQueue.replace_socket(self, socket)
        self.need_connection = False
        self.start_sending()


    def send_loop(self):
        '''
        Take items off the queue and put them on the network. Blocks 1 second
        if/when queue is empty and then returns
        '''
        while self.sending:
            try:
                item, id = self.queue.get(block=False)
                log.debug("trying to send: " + str(item))
            except Queue.Empty, e:
                self.sending = False
                log.info("send burst complete")
                return
            try:
                # send 6 bytes containing content length
                content_length = '0x%04x' % len(item)
                log.info(content_length)
                self.socket.send(content_length)
                # send json data
                self.socket.send(item)
                self.queue.mark_as_sent(id)
                log.debug("item sent")
            except:
                self.need_connection = True
                self.sending = False
                self.queue.put(item)
                log.info("socket broken")
                self.emit("socket-broken")


class NetworkInQueue(NetworkQueue):
    def __init__(self, socket, db):
        NetworkQueue.__init__(self, socket, DatabaseInQueue(db))

    def receive(self):
        ''' Receives data from network and puts it in a DatabaseQueue.

        This method blocks so using select before calling is good practice.
        '''
        if self.socket == None:
            self.emit("socket-broken")
            return 0, 0
        length = 0
        hex_length = ""
        try:
            hex_length = self.socket.recv(6)
            print type(hex_length), hex_length
            if hex_length == '':
                self.emit("socket-broken")
            length = int(hex_length, 16)
        except ValueError, e:
            print e
            self.emit("socket-broken")
            pass
        except socket.error:
            self.emit("socket-broken")

        if length == 0:
            log.info("Invalid content length: " + hex_length)
            self.emit("socket-broken")
            return 0, 0
        data = self.socket.recv(length)
        if data:
            log.debug("data from server:" + str(data))
            local_id = self.queue.put(data, 37)
            m = None
            try:
                m = shared.data.Message.unpack(data)
            except ValueError, ve:
                log.debug("Crappy data = ! JSON")
                log.debug(ve)
                return 0, 0

            return local_id, m.response_to

            # For now don't react on incoming messages directly from queue
            '''
            if m.type == shared.data.MessageType.login:
                self._login_client(s, m)
            else:
                self.message_handler.handle(m)
                self.message_available(data)
                '''
        else:
            self.emit("socket-broken")
            return 0, 0


    def dequeue(self):
        '''
        Pop an item from the queue. Raises Queue.Empty if empty. Does not block
        '''
        return self.queue.get(block=False)
        
    def get(self, message_id):
        queueItem = self.queue.peek(message_id)
        return queueItem
