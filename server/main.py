import gobject
import dbus.mainloop.glib
import select
import socket
import sys
import threading
import Queue
import dbus
import dbus.service

class Server(dbus.service.Object):
    input = [sys.stdin]

    def __init__(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("included.errors.Server", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus,
                                     '/Queue')
        self.host = ''
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.queue = Queue.Queue(10)

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
        print "opening socket"
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
        gobject.idle_add(mainloop.quit)
        # Wait for clients to exit
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
                    print "data from client:", data
                    self.queue.put(data, False)
                    print self.queue
                    sys.stdout.flush()
        
        print "Shutting down server"

    def dbusloop(self):
        #import signal
        #signal.signal(signal.SIGTERM, self.close)

        mainloop = gobject.MainLoop()
        print "Running example queue service."
        while mainloop.is_running():
            try:
                mainloop.run()
            except KeyboardInterrupt:
                mainloop.quit()


if __name__ == "__main__":
    s = Server()
    s.start()
