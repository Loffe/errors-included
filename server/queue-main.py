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
from shared.dbqueue import DatabaseInQueue
from shared.util import getLogger
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
        self.host = '127.0.0.1'
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.inqueue = DatabaseInQueue(self.db)
        self.outqueues = {}
        self.mainloop = None
        self.message_handler = handler.MessageHandler(self)

    @dbus.service.method(dbus_interface='included.errors.Server',
                         in_signature='ssi', out_signature='s')
    def enqueue(self, reciever, msg, prio):
        queue = self.outqueues[reciever]
        queue.enqueue(msg, prio)
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
            log.info("Could not open socket: " + message)
            sys.exit()

    def start(self):
        self.open_socket()
        self.input.append(self.server)
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

    def _accept_client(self, socket, port):
        self.input.append(socket)
        self.output.append(socket)
        self.outqueues[socket] = shared.networkqueue.NetworkOutQueue(socket, self.db)

    def _disconnect_client(self, socket):
        print "client disconnected"
        socket.close()
        try:
            self.input.remove(socket)
        except ValueError:
            print "Client not in input list. Why?"
        for id in self.outqueues.keys():
            if self.outqueues[id].socket == socket:
                del self.outqueues[id]

    def _login_client(self, socket, message):
        m = message
        if self.outqueues.has_key(socket):
            id = m.sender
            if self.db.is_valid_login(m.sender, m.unpacked_data["password"]):
                self.outqueues[id] = self.outqueues[socket]
                del self.outqueues[socket]
                
                self.set_ip(m.sender, socket.getpeername()[0])
                log.debug("logged in and now has a named queue")
                ack = shared.data.Message("server", id, response_to=m.message_id,
                                          type=shared.data.MessageType.login_ack,
                                          unpacked_data={"result": "yes", "class": "dict"})
                self.enqueue(m.sender, ack.packed_data, 5)
            else:
                log.debug("login denied")
                nack = shared.data.Message("server", id, response_to=m.message_id,
                                           type=shared.data.MessageType.login_ack,
                                           unpacked_data={"result": "no", "class": "dict"})
                # queue is not named because login failed
                self.enqueue(socket, nack.packed_data, 5)
                print "Login failed"
                #self._disconnect_client(socket)
        else:
            log.debug("no such socket or user already logged in")
            
    def set_ip(self, username, ip):
        session = self.db._Session()
        user = session.query(shared.data.UnitData).filter_by(name=username).first()
        user.ip = ip
        session.commit()
        print user, ip

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
                    if junk.startswith("quit"):
                        print "got quit"
                        running = False
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
                        local_id = self.inqueue.put(data)
                        m = None
                        try:
                            m = shared.data.Message.unpack(data)
                        except ValueError, ve:
                            log.debug("Crappy data = ! JSON")
                            log.debug(ve)
                            continue

                        if m.type == shared.data.MessageType.login:
                            self._login_client(s, m)
                        else:
                            self.message_received(local_id, m.response_to)
                    else:
                        self._disconnect_client(s)
        
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
    serverhandler = ServerNetworkHandler()
    serverhandler.start()
