import config
import dbus
import dbus.mainloop.glib
import dbus.service
import gobject
import select
import shared.data
import socket
import subprocess
import sys
import threading
import time
from shared.networkqueue import NetworkOutQueue, NetworkInQueue
from shared.util import getLogger
log = getLogger("queue.log")

class ClientNetworkHandler(dbus.service.Object):
    output = None
    input = None
    server = ()
    socket = None
    connected = False
    closing = False

    def __init__(self, host, port):
        log.info("Queue startin up")
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("included.errors.Client", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus,
                                     '/Queue')
        self.server = (host, port)
        self.db = shared.data.create_database()
        self.output = NetworkOutQueue(self.socket, self.db)
        self.input = NetworkInQueue(self.socket, self.db)
        self.inputs = [sys.stdin]

        self.input.connect("socket-broken", self._socket_broken)
        self.output.connect("socket-broken", self._socket_broken)

    @dbus.service.method(dbus_interface='included.errors.Client',
                         in_signature='si', out_signature='s')
    def enqueue(self, msg, prio):
        self.output.enqueue(msg, prio)
        #print "Queued: ", msg
        #print self.output
        return "Message queued :)"

    @dbus.service.method(dbus_interface='included.errors.Client',
                         in_signature='', out_signature='s')
    def dbus_close(self):
        self.close()
        return "queue closing"

    def connect_to_server(self):
        if not self.server:
            raise Exception("No server is set. Cannot connect")
        log.info("Connecting...")

        if config.server.ssh == True:
            subprocess.call(["ssh",
                             "-C", "-f",
                             "-L", str(config.server.localport)+":127.0.0.1:"+str(port),
                             host, "sleep", "10"])
            host = "127.0.0.1"
            port = config.server.localport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.server)
            self.connected = True
            self.closing = False
            self.inputs.append(self.socket)
            log.info("Connected :D")
            return True
        except socket.error, (errno, errmsg):
            self._handle_error(errno)
        return False

    def __del__(self):
        self.close()

    def close(self):
        log.info("Closing socket to server")
        if self.mainloop is not None:
            self.mainloop.quit()
        self.closing = True
        self.running = False
        self.socket.close()
        sys.exit(0)

    @dbus.service.signal(dbus_interface='included.errors.Client',
                         signature='')
    def message_received(self):
        #msg = self.input.dequeue()
        return

    def run(self):
        running = True
        while running:
            inputready, outputready, exceptready = select.select(
                    self.inputs, [], [], 1.0)
            if len(inputready) > 0:
                print "got input from", inputready
            for s in inputready:
                if s == sys.stdin:
                    junk = sys.stdin.readline()
                    if junk == '':
                        self.inputs.remove(s)
                    if junk.startswith("quit"):
                        print "got quit"
                        running = False
                    else:
                        print "got", junk
                elif s == self.socket:
                    print "gettin' msg"
                    self.input.receive()
                    print "Just putted a message in a queue :D"
        self.close()

    def mainloop(self):
        self._check_connection()
        def _sigterm_cb(self):
            gobject.idle_add(self.close)
        import signal
        signal.signal(signal.SIGTERM, _sigterm_cb)

        threading.Thread(target=self.run).start()

        gobject.threads_init()
        self.mainloop = mainloop = gobject.MainLoop()
        print "Running example queue service."
        mainloop.run()
        while mainloop.is_running():
            try:
                mainloop.run()
            except KeyboardInterrupt:
                self.close()

    def _check_connection(self):
#        print "_check_connection"
        if self.closing == True:
            return False
        if self.connected == True:
            return True
        else:
            result = self.connect_to_server()
            if result:
                self.output.replace_socket(self.socket)
                self.input.replace_socket(self.socket)
            else:
                gobject.timeout_add(config.queue.reconnect_interval,
                                    self._check_connection)
            return False

    def _socket_broken(self, event):
        print "socket-broken"
        if self.connected:
            self.connected = False
            self.inputs.remove(self.socket)
            threading.Thread(target=self._check_connection()).start()


    def _handle_error(self, errno, errmsg=None):
        if errno == 111:
            pass
#            print "Connection refused"
        else:
            print errno, errmsg
