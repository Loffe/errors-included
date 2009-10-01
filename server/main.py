
import select
import socket
import sys
import threading

all = []

class Server:
    def __init__(self):
        self.host = ''
        self.port = 50000
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(5)
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            print "Could not open socket: " + message
            sys.exit()

    def run(self):
        global all
        self.open_socket()
        input = [self.server, sys.stdin]
        running = True
        while running:
            inputready, outputready, exceptready = select.select(input, [], [])
            for s in inputready:
                if s == self.server:
                    c = Client(self.server.accept())
                    c.start()
                    self.threads.append(c)
                    all.append(c)
                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    running = False

        print "Shutting down server"
        self.server.close()
        # Wait for clients to exit
        for c in self.threads:
            c.join()

class Client(threading.Thread):
    def __init__(self, (client, address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024

    def run(self):
        global all
        running = True
        while running:
            data = self.client.recv(self.size)
            if data:
                self.send_message(data)
                for c in all:
                    if c != self:
                        c.send_message(data)
                print data
            else:
                self.client.close()
                all.remove(self)
                running = False

    def send_message(self, message):
        global all
        try:
            self.client.send(message)
        except socket.error, (value, message):
            print (value, message)
            all.remove(self)


if __name__ == "__main__":
    s = Server()
    s.run()
