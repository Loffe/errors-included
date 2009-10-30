import socket
import threading
import time

class Queue(threading.Thread):
    output = []
    input = []
    socket = None
    running = False

    def __init__(self):
        pass

    def enqueue(self, msg):
        self.output.append(msg)

    def connect_to_server(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.running = True

    def close(self):
        self.socket.close()

    def mainloop(self):
        t = threading.Thread(target=self.listener)
        t.start()
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

