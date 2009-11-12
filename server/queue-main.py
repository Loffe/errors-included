import gobject
import dbus.mainloop.glib
import select
import socket
import sys
import threading
import Queue
import dbus
import dbus.service
import shared.networkqueue
from shared.util import getLogger
log = getLogger("server.log")
import shared.data
import handler

class ServerNetworkHandler(dbus.service.Object):
    input = [sys.stdin]
    output = []
    message_handler = None

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("included.errors.Server", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus,
                                     '/Queue')
        self.host = '127.0.0.1'
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.inqueue = Queue.Queue()
        self.outqueues = {}
        self.mainloop = None
        self.message_handler = handler.MessageHandler(self)

    @dbus.service.method(dbus_interface='included.error.Server',
                         in_signature='sv', out_signature='s')
    def enqueue(self, reciever, msg):
        try:
            queue = self.outqueues[reciever]
        except KeyError:
            queue = self.outqueues[reciever] = Queue.Queue()
        queue.put(queue, msg)
        print "Enqueue called"
        return "Enqueue :)"

    @dbus.service.method(dbus_interface='included.error.Server',
                         in_signature='v', out_signature='s')
    def dequeue(self, variant):
        print "Popped called"
        return "Popped :)"

    @dbus.service.signal(dbus_interface='included.error.Server',
                         signature='s')
    def message_available(self, string):
        print "Message Available!!"
        return "Message Available!!"

    def open_socket(self):
        log.info("Server is opening socket")
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if 'arm' not in sys.version.lower():
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            print "Listening on port %s" % self.port
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            log.info("Could not open socket: " + message)
            sys.exit()

    def start(self):
        self.open_socket()
        self.input.append(self.server)
        threading.Thread(target=self.run).start()
        #gobject.idle_add(self.run)
        self.dbusloop()

    def close(self):
        log.info("Shutting down server")
        if self.mainloop:
            gobject.idle_add(self.mainloop.quit)
        # Wait for clients to exit
        self.server.close()
        for s in self.input:
            s.close()

    def _accept_client(self, socket, port):
        self.input.append(socket)
        self.output.append(socket)
        self.outqueues[socket] = shared.networkqueue.NetworkOutQueue(socket)

    def run(self):
        running = True
        while running:
            inputready, outputready, exceptready = select.select(self.input, [], [])
            print "got input"
            for s in inputready:
                if s == self.server:
                    (client, port) = self.server.accept()
                    print "client connected from ", port
                    self._accept_client(client, port)
                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    if junk.startswith("quit"):
                        print "got quit"
                        running = False
                else:
                    # read and parse content length
                    length = 0
                    try:
                        hex_length = s.recv(6)
                        length = int(hex_length, 16)
                    except ValueError:
                        pass

                    if length == 0:
                        log.info("Invalid content length: ", hex_length)
                        continue
                    data = s.recv(length)
                    if data:
                        self.message_available("super message is here")
                        log.debug("data from client:" + str(data))
                        self.inqueue.put(data, False)
                        m = None
                        try:
                            m = shared.data.Message(None, None, packed_data=data)
                        except ValueError, ve:
                            log.debug("Crappy data = ! JSON")
                            log.debug(ve)
                            continue

                        self.message_handler.handle(m)
                    else:
                        print "client disconnected"
                        s.close()
                        self.input.remove(s)
                        self.output.remove(s)
        
        self.close()

    def dbusloop(self):
        #import signal
        #signal.signal(signal.SIGTERM, self.close)

        self.mainloop = gobject.MainLoop()
        gobject.threads_init()

        print "Running example queue service."
        while self.mainloop.is_running():
            try:
                self.mainloop.run()
            except KeyboardInterrupt:
                self.mainloop.quit()


if __name__ == "__main__":
    s = ServerNetworkHandler()
    s.start()
