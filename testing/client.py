#!/usr/bin/env python 
import socket, sys

host = '130.236.189.24'
port = 50000
size = 1024
s = None
try:
    sshpipe = os.popen("ssh -C -N -f -L 50001:127.0.0.1:50000 127.0.0.1")
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
sshpipe.close()
