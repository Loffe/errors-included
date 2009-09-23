#!/usr/bin/env python 

import socket, sys

#host = ''
port = 50001
#backlog = 5
size = 1024
s = None
data = ''
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('',port))
	s.listen(5)
except socket.error, (value,message):
	if s:
		s.close()
	print 'Could not open socket. '+message
	sys.exit(1)

while data != 'close':
	client, address = s.accept()
	print address
	data = client.recv(size)
	if data:
		# return the data
		client.send(data)
		print data
		client.close()
s.close()
