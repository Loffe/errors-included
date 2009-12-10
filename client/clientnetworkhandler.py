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
    use_backup = False

    def __init__(self):
        log.info("Queue startin up")
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.session_bus = dbus.SessionBus()
        self.name = dbus.service.BusName("included.errors.Client", self.session_bus)
        dbus.service.Object.__init__(self, self.session_bus,
                                     '/Queue')
        self.db = shared.data.create_database()
        self.output = NetworkOutQueue(self.socket, self.db, config.client.name)
        self.input = NetworkInQueue(self.socket, self.db)
        self.inputs = [sys.stdin]

        self.input.connect("socket-broken", self._socket_broken)
        self.output.connect("socket-broken", self._socket_broken)

    @dbus.service.method(dbus_interface='included.errors.Client',
                         in_signature='si', out_signature='i')
    def enqueue(self, msg, prio):
        local_id = self.output.enqueue(msg, prio)
        #print "Queued: ", msg
        #print self.output
        return local_id

    @dbus.service.method(dbus_interface='included.errors.Client',
                         in_signature='', out_signature='s')
    def dbus_close(self):
        self.close()
        return "queue closing"

    def connect_to_server(self):
        log.info("Connecting to %s..." % ("primary", "backup")[self.use_backup])
        if self.use_backup:
            host = config.server.backup.ip
            port = config.server.backup.port
        else:
            host = config.server.ip
            port = config.server.port

        if config.server.ssh == True:
            ssh_options = ["ssh",
                             "-C", "-f",
                             "-L", str(config.server.localport)+":127.0.0.1:"+str(port),
                             host, "-o", "TCPKeepAlive=yes", "sleep", "10"]
            print " ".join(ssh_options)
            subprocess.call(ssh_options)
            host = "127.0.0.1"
            port = config.server.localport
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
            self.connected = True
            self.closing = False
            self.inputs.append(self.socket)
            self._login()
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
                         signature='ii')
    def message_received(self, local_id, response_to):
        if response_to == self.login_msg_id:
            print "got a login ack"
            data = self.input.get(local_id)
            ack = shared.data.Message.unpack(data, self.db)
            if ack.unpacked_data["result"] == "yes":
                print "Login ok"
            elif ack.unpacked_data["result"] == "no":
                print "Couldn't login. Please check username/password"
                self.close()
            elif ack.unpacked_data["result"] == "try_primary":
                print "Primary is still alive"
                self.close()
            else:
                print "Other random login failure"
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
                    if junk.startswith("q"):
                        print "got quit"
                        running = False
                    else:
                        print "got", junk
                elif s == self.socket:
                    print "gettin' msg"
                    local_id, response_to = self.input.receive()
                    print "Just putted a message %s in response to %s" % (local_id, response_to)
                    self.message_received(local_id, response_to)
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
        #print "_check_connection"
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
            print "Connection refused"
            self.use_backup = not self.use_backup
        else:
            print errno, errmsg

    def _login(self):
        login_msg = shared.data.Message(config.client.name, "server",
                                        type=shared.data.MessageType.login,
                                        unpacked_data={"class": "dict",
                                            "unit_type":config.client.type,
                                            "password":config.client.password})
        self.login_msg_id = self.enqueue(login_msg.packed_data, 9)

