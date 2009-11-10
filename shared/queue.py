import config
import dbus
import dbus.mainloop.glib
import dbus.service
import gobject
import socket
import subprocess
import threading
import time
from shared.util import getLogger
log = getLogger("queue.log")

class Queue(dbus.service.Object):
    output = []
    input = []
    server = ()
    socket = None
    running = False
    closing = False

    def __init__(self, host, port):
        log.info("Queue startin up")
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("com.example.Queue", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus,
                                     '/Queue')
        self.server = (host, port)

    @dbus.service.method(dbus_interface='com.example.Queue',
                         in_signature='v', out_signature='s')
    def enqueue(self, msg):
        self.output.append(msg)
        #print "Queued: ", msg
        #print self.output
        return "message queued :)"

    @dbus.service.method(dbus_interface='com.example.Queue',
                         in_signature='', out_signature='s')
    def dbus_close(self):
        self.close()
        return "queue closing"

    def connect_to_server(self):
        if not self.server:
            raise Exception("No server is set. Cannot connect")
        log.info("Connecting")

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
            self.running = True
            self.closing = False
            log.info("Connected :D")
            self.thread_listen = threading.Thread(target=self._recv)
            self.thread_send = threading.Thread(target=self._send)
            self.thread_listen.start()
            self.thread_send.start()
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

    def _send(self):
        log.info("starting send loop" + str(self.output))
        while self._check_connection():
            if len(self.output) > 0:
                msg = self.output[0]
                self.socket.send(msg)
                del self.output[0]

    def _recv(self):
        print "starting listen loop"
        self.socket.settimeout(1.0)
        while self._check_connection():
            try:
                data = self.socket.recv(1000)
            except socket.timeout:
                return True
            self.input.append(data)

    def mainloop(self):
        if self._check_connection():
            gobject.idle_add(self._send)
            gobject.idle_add(self._recv)

        def _sigterm_cb(self):
            gobject.idle_add(self.close)
        import signal
        signal.signal(signal.SIGTERM, _sigterm_cb)

        self.mainloop = mainloop = gobject.MainLoop()
        print "Running example queue service."
        while mainloop.is_running():
            try:
                mainloop.run()
            except KeyboardInterrupt:
                self.close()

    def _check_connection(self):
        print "_check_connection"
        if self.closing == True:
            return False
        if self.running == True:
            return True
        if not self.connect_to_server():
            gobject.timeout_add(config.queue.reconnect_interval, self._check_connection)

    def _handle_error(self, errno, errmsg=None):
        if errno == 111:
            print "Connection refused"
        else:
            print errno, errmsg
