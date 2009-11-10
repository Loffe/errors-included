import gobject
import threading
import Queue

import shared.data

from shared.util import getLogger
log = getLogger("server.log")

class NetworkQueue(object):
    queue = Queue.Queue()

    def __init__(self, socket):
        self.socket = socket

class NetworkOutQueue(object):
    sending = False

    def __init__(self, socket):
        NetworkQueue.__init__(self, socket)

    def enqueue(self, msg):
        data = msg.packed_data
        self.queue.put(data)
        if not self.sending:
            self.start_sending()

    def start_sending(self):
        '''
        Starts a send burst in a new thread
        '''
        self.sending = true
        threading.Thread(target=self.send_loop).start()


    def send_loop(self):
        '''
        Take items off the queue and put them on the network. Blocks 1 second
        if/when queue is empty and then returns
        '''
        while self.sending:
            try:
                item = self.queue.get(timeout=1)
                self.socket.write(item)
            except Queue.Empty, e:
                return


class NetworkInQueue(object):
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
        
