import gobject
import socket
import threading
import time
import dbus
import dbus.service
import dbus.mainloop.glib

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
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.running = True

    def close(self):
        self.socket.close()

    def mainloop(self):
        t = threading.Thread(target=self.listener)
        t.start()
        dbus_t = threading.Thread(target=self.dbus_main)
        dbus_t.start()
        #self.dbus_main()

        while self.running:
            if len(self.output) > 0:
                msg = self.output.pop()
                self.socket.send(msg)

        self.socket.close()

    def listener(self):
        self.socket.settimeout(1.0)
        while self.running:
            try:
                data = self.socket.recv(1000)
            except socket.timeout:
                continue
            self.input.append(data)


    def dbus_main(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

        session_bus = dbus.SessionBus()
        name = dbus.service.BusName("com.example.Queue", session_bus)
        object = Queue(session_bus, '/Queue')

        mainloop = gobject.MainLoop()
        print "Running example queue service."
        mainloop.run()
