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

    def send(self, msg):
        self.out.append(msg)

    def connect_to_server(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host,port))
        self.running = True

    def mainloop(self):
        t = threading.Thread(target=self.listener)
        t.start()
        i = 0
        while self.running:
            self.socket.send("Hejsan" + str(i))
            i+=1
            time.sleep(1)

        self.socket.close()

    def listener(self):
        while self.running:
            data = self.socket.recv(1000)
            print data
            if data == "Hejsan10":
                self.running = False

