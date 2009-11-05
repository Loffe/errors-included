import config
import dbus
import dbus.mainloop.glib
import dbus.service
import gobject
import socket
import subprocess
import threading
import time

class Queue(dbus.service.Object):
    output = []
    input = []
    server = ()
    socket = None
    running = False

    def __init__(self, host, port):
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
        print "Queued: ", msg
        return "message queued :)"

    def connect_to_server(self):
        if not self.server:
            raise Exception("No server is set. Cannot connect")
        print "Connecting"

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
            gobject.idle_add(self._send)
            gobject.idle_add(self._recv)
            print "Connected :D"
        except socket.error, (errno, errmsg):
            self._handle_error(errno)
        return False

    def __del__(self):
        self.close()

    def close(self):
        print "Closing socket to server"
        self.socket.close()

    def _send(self):
        if not self._check_connection():
            return
        if len(self.output) > 0:
            msg = self.output.pop()
            self.socket.send(msg)
        return True

    def _recv(self):
        if not self._check_connection():
            return
        self.socket.settimeout(1.0)
        try:
            data = self.socket.recv(1000)
        except socket.timeout:
            return True
        self.input.append(data)
        return True

    def mainloop(self):
        if self._check_connection():
            gobject.idle_add(self._send)
            gobject.idle_add(self._recv)

        def _sigterm_cb(self):
            gobject.idle_add(mainloop.quit)
        import signal
        signal.signal(signal.SIGTERM, _sigterm_cb)

        mainloop = gobject.MainLoop()
        print "Running example queue service."
        while mainloop.is_running():
            try:
                mainloop.run()
            except KeyboardInterrupt:
                mainloop.quit()

    def _check_connection(self):
        if self.running == True:
            return True
        if not self.connect_to_server():
            gobject.timeout_add(config.queue.reconnect_interval, self._check_connection)

    def _handle_error(self, errno, errmsg=None):
        if errno == 111:
            print "Connection refused"
