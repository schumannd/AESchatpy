#!/usr/bin/python 

from socket import socket
import thread

davidsSocket = socket()
host = '127.0.0.1'
port = 1233
BUFFERSIZE = 1024

# def send(connection):

def recieve(connection):
	while True:
		data = connection.recv(BUFFERSIZE)
		print data

davidsSocket.connect((host,port))
thread.start_new_thread(recieve, (davidsSocket,))
while True:
	data = raw_input('')
	if not data: break
	davidsSocket.send(data)
# thread.start_new_thread(send, (davidsSocket,))
davidsSocket.close