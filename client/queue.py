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
    socket = None
    running = False

    @dbus.service.method(dbus_interface='com.example.Queue',
                         in_signature='v', out_signature='s')
    def enqueue(self, msg):
        self.output.append(msg)
        return "message queued :)"

    def connect_to_server(self, host, port):
        if config.server.ssh == True:
            subprocess.call(["ssh",
                             "-C", "-f",
                             "-L", str(config.server.localport)+":127.0.0.1:"+str(port),
                             host, "sleep", "10"])
            host = "127.0.0.1"
            port = config.server.localport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.running = True

    def __del__(self):
        self.close()

    def close(self):
        print "Closing socket to server"
        self.socket.close()

    def _send(self):
        if len(self.output) > 0:
            msg = self.output.pop()
            self.socket.send(msg)
        return True

    def _recv(self):
        self.socket.settimeout(1.0)
        try:
            data = self.socket.recv(1000)
        except socket.timeout:
            return True
        self.input.append(data)
        return True

    def mainloop(self):
        gobject.idle_add(self._send)
        gobject.idle_add(self._recv)

        def _sigterm_cb(self):
            gobject.idle_add(mainloop.quit)
        import signal
        signal.signal(signal.SIGTERM, _sigterm_cb)

        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("com.example.Queue", session_bus)
        object = Queue(session_bus, '/Queue')

        mainloop = gobject.MainLoop()
        print "Running example queue service."
        while mainloop.is_running():
            try:
                mainloop.run()
            except KeyboardInterrupt:
                mainloop.quit()
