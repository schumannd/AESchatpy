#!/usr/bin/python

from socket import socket
import thread

clients = []
serverSocket = socket()
host = '127.0.0.1'
port = 1233
BUFFERSIZE = 1024
serverSocket.bind((host,port))
serverSocket.listen(5)

def newClient(connection):
	print "Got connection from", addr
	connection.send("Thank you for connecting!")
	while True:
		message = connection.recv(BUFFERSIZE)
		if not message: return
		for client in clients:
			if connection != client[1]:
				client[1].send(str(client[0])+": "+message)


while True:
	connection, addr = serverSocket.accept()
	clients.append([addr, connection])
	thread.start_new_thread(newClient, (connection,))