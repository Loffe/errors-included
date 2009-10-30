import socket
import threading

class Queue(threading.Thread):
    output = []
    input = []
    socket = None

    def __init__(self):
        pass

    def send(self, msg):
        self.out.append(msg)

    def connect_to_server(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
