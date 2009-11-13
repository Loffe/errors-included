import gobject
import threading
import Queue

import shared.data
from shared.dbqueue import DatabaseQueue

from shared.util import getLogger
log = getLogger("nw-queue.log")

class NetworkQueue(gobject.GObject):
    queue = None
    socket = None

    def __init__(self, socket, db, direction):
        self.__gobject_init__()
        self.socket = socket
        self.queue = DatabaseQueue(db, direction)

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
        NetworkQueue.__init__(self, socket, db, DatabaseQueue.direction_out)
        if self.socket:
            self.need_connection = False

    def enqueue(self, packed_data, prio):
        print "enqueued"
        self.queue.put(packed_data, prio)
        if not self.sending:
            self.start_sending()

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
                item = self.queue.get(block=False)
                log.debug("trying to send: " + item)
            except Queue.Empty, e:
                self.sending = False
                log.info("send burst complete")
                return
            try:
                # send 6 bytes containing content length
                self.socket.send('0x%04x' % len(item))
                # send json data
                self.socket.send(item)
                self.queue.mark_as_sent(item)
                log.debug("item sent")
            except:
                self.need_connection = True
                self.sending = False
                self.queue.put(item)
                log.info("socket broken")
                self.emit("socket-broken")


class NetworkInQueue(NetworkQueue):
    def __init__(self, socket, db):
        NetworkQueue.__init__(self, socket, db, DatabaseQueue.direction_in)

    def receive(self):
        data = self.socket.recv(1024)
        self.queue.put(data)


    def dequeue(self):
        '''
        Pop an item from the queue. Raises Queue.Empty if empty. Does not block
        '''
        return self.queue.get(block=False)
        
