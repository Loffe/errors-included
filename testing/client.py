#!/usr/bin/env python 

import socket, sys

host = 'localhost'
port = 50001
size = 2048
s = None
while True:
	data = raw_input()
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host,port))
	except socket.error, (value,message):
		if s:
			s.close()
		print 'Could not open socket: ' + message
		sys.exit(1)

	s.send(data)
	data = s.recv(size)
	print 'Recieved:', data
	s.close()
	
	
