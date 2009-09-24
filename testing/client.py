#!/usr/bin/env python 

import socket, sys

host = 'localhost'
port = 50000
size = 2048
s = None
while True:
    send_data = raw_input("Say: ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host,port))
    except socket.error, (value,message):
        if s:
            s.close()
        print 'Could not open socket: ' + message
        sys.exit(1)

    s.send(send_data)
    recv_data = s.recv(size)
    print 'Recieved:', recv_data
    s.close()