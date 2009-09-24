#!/usr/bin/env python 
import socket, sys

host = 'localhost'
port = 50000
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
except socket.error, (value,message):
    if s:
        s.close()
    print 'Could not open socket: ' + message
    sys.exit(1)

send_data = ""
while send_data != "close":
    send_data = raw_input("Say: ")

    if len(send_data) <= 1:
        continue
    s.send(send_data)
    recv_data = s.recv(size)
    print 'Recieved:', recv_data

s.close()
