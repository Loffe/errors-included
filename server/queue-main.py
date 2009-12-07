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
import config
from shared.dbqueue import DatabaseInQueue
from shared.util import getLogger
from shared.networkqueue import NetworkOutQueue
from database import ServerDatabase
log = getLogger("server.log")
import shared.data
import handler
import data

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
        db = ServerDatabase()
        self.db = shared.data.create_database(db)
        if config.server.ssh:
            self.host = '127.0.0.1'
        else:
            self.host = ''
        self.port = config.server.port
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.inqueue = DatabaseInQueue(self.db)
        self.outqueues = {}
        self._init_queues()
        self.mainloop = None
        self.message_handler = handler.MessageHandler(self)
        if config.server.primary == False:
            self.primary_alive = False

    @dbus.service.method(dbus_interface='included.errors.Server',
                         in_signature='ssi', out_signature='s')
    def enqueue(self, reciever, msg, prio):
        '''
        @param reciever the name of the unit to send to
        @param msg the packed_data to send
        @param prio priority of the message
        '''
        queue = self.outqueues[reciever]
        queue.enqueue(unicode(msg), prio)
        print "Enqueue called"
        return "Enqueue :)"

    @dbus.service.method(dbus_interface='included.errors.Server',
                         in_signature='v', out_signature='s')
    def dequeue(self, variant):
        print "Popped called"
        return "Popped :)"

    @dbus.service.signal(dbus_interface='included.errors.Server',
                         signature='ii')
    def message_received(self, local_id, response_to):
        print "Message Available!!"
        return "Message Available!!"

    @dbus.service.signal(dbus_interface='included.errors.Server',
                         signature='s')
    def user_login(self, username):
        print "Login from", username

    def open_socket(self):
        log.info("Server is opening socket")
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if 'arm' not in sys.version.lower():
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
            self.input.append(self.server)
            print "Listening on port %s" % self.port
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            log.info("Could not open socket: " + message)
            sys.exit()

    def start(self):
        if config.server.primary:
            self.open_socket()
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

    def _init_queues(self):
        users = self.db.get_all_users()
        for u in users:
            self.outqueues[u.name] = NetworkOutQueue(None, self.db, u.name)

        if config.server.primary:
            print "starting heartbeat"
            self.heartbeat_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if 'arm' not in sys.version.lower():
                self.heartbeat_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.heartbeat_socket.bind((self.host, config.primary.heartbeatport))
            self.heartbeat_socket.listen(5)
            self.input.append(self.heartbeat_socket)
        else:
            self.heartbeat_socket = None
            self.ping()
        print self.outqueues

    def _accept_client(self, socket, port):
        self.input.append(socket)
        self.output.append(socket)

    def _disconnect_client(self, socket):
        print "client disconnected"
        socket.close()
        try:
            self.input.remove(socket)
        except ValueError:
            print "Client not in input list. Why?"

    def _login_client(self, socket, message):
        m = message
        id = m.sender
        if self.db.is_valid_login(m.sender, m.unpacked_data["password"]):
            self.outqueues[id].replace_socket(socket)
            
            log.info("%s logged in and now has a named queue" % id)
            ack = shared.data.Message("server", id, response_to=m.message_id,
                                      type=shared.data.MessageType.ack,
                                      unpacked_data={"result": "yes", "class": "dict"})
            self.enqueue(m.sender, ack.packed_data, 9)
            self.user_login(m.sender)
        else:
            log.info("login denied")
            nack = shared.data.Message("server", id, response_to=m.message_id,
                                       type=shared.data.MessageType.ack,
                                       unpacked_data={"result": "no", "class": "dict"})
            # queue is not named because login failed
            self.enqueue(m.sender, nack.packed_data, 9)
            print "Login failed"
            #self._disconnect_client(socket)
            

    def run(self):
        running = True
        while running:
            inputready, outputready, exceptready = select.select(self.input, [], [])
            print "got input"
            for s in inputready:
                if s == self.server:
                    (client, port) = self.server.accept()
                    print "client connected from ", port
                    # put client in temp list based on socket
                    self._accept_client(client, port)
                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    if junk.startswith("q"):
                        print "got quit"
                        running = False
                elif s == self.heartbeat_socket:
                    print "got heartbeat"
                    data = None
                    (pinger, port) = s.accept()
                    try:
                        data = pinger.recv(4)
                        if data == "ping":
                            print "got ping => pong"
                        pinger.send("pong")
                    except socket.error, e:
                        print e
                    pinger.close()
                else:
                    # read and parse content length
                    length = 0
                    try:
                        hex_length = s.recv(6)
                        length = int(hex_length, 16)
                    except ValueError:
                        pass
                    except socket.error:
                        self._disconnect_client(s)

                    if length == 0:
                        log.info("Invalid content length: " + hex_length)
                        self._disconnect_client(s)
                        continue
                    data = s.recv(length)
                    if data:
                        log.debug("data from client:" + str(data))
                        local_id = self.inqueue.put(unicode(data))
                        m = None
                        try:
                            m = shared.data.Message.unpack(data, self.db)
                        except ValueError, ve:
                            log.info("Crappy data = ! JSON")
                            log.info(ve)
                            continue

                        if m.type == shared.data.MessageType.login:
                            self._login_client(s, m)
                        else:
                            self.message_received(local_id, m.response_to)
                    else:
                        self._disconnect_client(s)
        
        self.close()

    def ping(self):
        print "Sent heatbeat, duh-duh..."
        response = None
        try:
            self.primary_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.primary_socket.connect((config.primary.ip, config.primary.heartbeatport))
            self.primary_socket.send("ping")
            response = self.primary_socket.recv(4)
            self.primary_socket.close()
        except Exception, e:
            print "Exception during heartbeat", e
        self.primary_alive = response == "pong"
        if self.primary_alive:
            print "Primary is alive"
            gobject.timeout_add(config.primary.heartbeatinterval, self.ping)
        else:
            print "Primary is dead! I'm in command!"
            self.open_socket()

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
    serverhandler = ServerNetworkHandler()
    serverhandler.start()
