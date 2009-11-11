import gobject
import threading
import Queue

import shared.data

from shared.util import getLogger
log = getLogger("nw-queue.log")

class NetworkQueue(object):
    queue = Queue.Queue()
    socket = None

    def __init__(self, socket):
        self.socket = socket

    def replace_socket(self, socket):
        print self.__class__.__name__, "got a new socket"
        self.socket = socket

class NetworkOutQueue(NetworkQueue):
    sending = False

    def __init__(self, socket):
        NetworkQueue.__init__(self, socket)

    def enqueue(self, packed_data):
        print "enqueued"
        self.queue.put(packed_data)
        if not self.sending:
            self.start_sending()

    def start_sending(self):
        '''
        Starts a send burst in a new thread
        '''
        print "starting send burst"
        self.sending = True
        threading.Thread(target=self.send_loop).start()

    def replace_socket(self, socket):
        NetworkQueue.replace_socket(self, socket)
        self.start_sending()


    def send_loop(self):
        '''
        Take items off the queue and put them on the network. Blocks 1 second
        if/when queue is empty and then returns
        '''
        while self.sending:
            try:
                item = self.queue.get(block=False)
                log.info("sending" + item)
            except Queue.Empty, e:
                self.sending = False
                return
            try:
                self.socket.send(item)
            except:
                self.need_connection = False
                self.queue.put(item)


class NetworkInQueue(NetworkQueue):
    def __init__(self, socket, callback):
        NetworkQueue.__init__(self, socket)
        self.callback = callback

    def receive(self):
        data = self.socket.recv(1024)
        self.queue.put(data)
        self.callback()


    def dequeue(self):
        '''
        Pop an item from the queue. Raises Queue.Empty if empty. Does not block
        '''
        return self.queue.get(block=False)
        
