#!/usr/bin/python
import sys
import copy
from socket import socket
from numberTheory import *
import thread

clients = []
serverSocket = socket()
host = '127.0.0.1'
port = 1234
BUFFERSIZE = 1024
serverSocket.bind((host,port))
serverSocket.listen(5)
publicElGamalKeys = []		# [p, g, b]
privateElGamalKey = 0

def main():
	while True:
		connection, address = serverSocket.accept()
		thread.start_new_thread(newClient, (connection, address))

def readInKeys():
	global publicElGamalKeys
	global privateElGamalKey
	with open("id_elgamal.pub", "r") as publicKeyFile:
		publicElGamalKeys = publicKeyFile.read().split("\n")
	with open("id_elgamal", "r") as privateKeyFile:
		privateElGamalKey = int(privateKeyFile.read())

def sendPublicKeys(connection):
	connection.send("\n".join(publicElGamalKeys))
	connection.send("done")

def decryptSharedSecret(c1, c2):
	p = int(publicElGamalKeys[0])
	s = pow(c1, privateElGamalKey, p)
	message = c2 * modularInverse(s, p) % p
	return message

def exchangeSecret(connection):
	sendPublicKeys(connection)
	encryptedSecretC1 = int(connection.recv(BUFFERSIZE))
	encryptedSecretC2 = int(connection.recv(BUFFERSIZE))
	return decryptSharedSecret(encryptedSecretC1, encryptedSecretC2)

def newClient(connection, address):
	readInKeys()
	print "Got connection from.", address, " exchanging secret"
	sharedSecret = exchangeSecret(connection)
	connection.send("Thank you for connecting! Handshake complete")
	clients.append([address, connection, sharedSecret])

	while True:
		message = connection.recv(BUFFERSIZE)
		if not message: return
		for client in clients:
			if connection != client[1]:
				client[1].send(str(client[0])+": "+message)

if __name__ == "__main__":
	sys.exit(main())