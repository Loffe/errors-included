import config
import dbus
import dbus.mainloop.glib
import dbus.service
import gobject
import socket
import subprocess
import threading
import time
from networkqueue import NetworkOutQueue, NetworkInQueue
from shared.util import getLogger
log = getLogger("queue.log")
log.debug("hej")

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
        self.name = dbus.service.BusName("com.example.Queue", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus,
                                     '/Queue')
        self.server = (host, port)
        self.output = NetworkOutQueue(self.socket)
        self.input = NetworkInQueue(self.socket, self.message_received)

        self.output.connect("socket-broken", self._socket_broken)

    @dbus.service.method(dbus_interface='com.example.Queue',
                         in_signature='v', out_signature='s')
    def enqueue(self, msg):
        self.output.enqueue(msg)
        #print "Queued: ", msg
        #print self.output
        return "Message queued :)"

    @dbus.service.method(dbus_interface='com.example.Queue',
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
        self.socket.close()

    @dbus.service.signal(dbus_interface='com.example.Queue',
                         signature='')
    def message_received(self):
        #msg = self.input.dequeue()
        return

    def mainloop(self):
        self._check_connection()
        def _sigterm_cb(self):
            gobject.idle_add(self.close)
        import signal
        signal.signal(signal.SIGTERM, _sigterm_cb)

        gobject.threads_init()
        self.mainloop = mainloop = gobject.MainLoop()
        print "Running example queue service."
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
        self.connected = False
        self._check_connection()


    def _handle_error(self, errno, errmsg=None):
        if errno == 111:
            pass
#            print "Connection refused"
        else:
            print errno, errmsg
