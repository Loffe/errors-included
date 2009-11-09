import gobject
import dbus.mainloop.glib
import select
import socket
import sys
import threading
import Queue
import dbus
import dbus.service
from shared.util import log as log

class Server(dbus.service.Object):
    input = [sys.stdin]

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
        self.outqueue = Queue.Queue()
        self.mainloop = None

    @dbus.service.enqueue(dbus_interface='included.error.Server',
                         in_signature='v', out_signature='s')
    def enqueue(self, variant):
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
            print "Could not open socket: " + message
            sys.exit()

    def start(self):
        self.open_socket()
        self.input.append(self.server)
        threading.Thread(target=self.run).start()
        #gobject.idle_add(self.run)
        self.dbusloop()

    def close(self):
        print "Shutting down server"
        if self.mainloop:
            gobject.idle_add(self.mainloop.quit)
        # Wait for clients to exit
        self.server.close()
        for s in self.input:
            s.close()

    def run(self):
        running = True
        while running:
            inputready, outputready, exceptready = select.select(self.input, [], [])
            print "got input"
            for s in inputready:
                if s == self.server:
                    (client, port) = self.server.accept()
                    self.input.append(client)
                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    if junk.startswith("quit"):
                        print "got quit"
                        running = False
                else:
                    data = s.recv(1024)
                    if data:
                        self.message_available("super message is here")
                        log.debug("data from client:" + str(data))
                        self.inqueue.put(data, False)
                        print self.inqueue
                        sys.stdout.flush()
                    else:
                        s.close()
                        self.input.remove(s)
        
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
    s = Server()
    s.start()
