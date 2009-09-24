#!/usr/bin/env python 

import socket, sys

host = ''
port = 50000
backlog = 5
size = 1024
s = None
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host,port))
    s.listen(backlog)
except socket.error, (value,message):
    if s:
        s.close()
    print 'Could not open socket. ' + message
    sys.exit(1)

recv_data = ''
send_data = ''
while recv_data != 'close':
    client, address = s.accept()
    recv_data = client.recv(size)
    if recv_data:
        if recv_data == 'close':
            send_data = 'closing server'
        elif recv_data == 'ping':
            send_data = 'pong'
        else:
            send_data = recv_data
        client.send(send_data)
        client.close()
        print address[0], "says:", recv_data
        print "Sent:", send_data
s.close()