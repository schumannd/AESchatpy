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

def newClient(connection, address):
	readInKeys()
	print "# Got connection from.", address, " exchanging secret"
	sharedSecret = exchangeSecret(connection)
	connection.send("# Thank you for connecting! Handshake complete")
	clients.append([address, connection, sharedSecret])
	sendReceiveLoop(connection, sharedSecret)

def sendReceiveLoop(connection, sharedSecret):
	while True:
		encryptedMessage = connection.recv(BUFFERSIZE)
		if not encryptedMessage: return
		message = decryptAES(encryptedMessage, sharedSecret)
		for client in clients:
			if connection != client[1]:
				reEncryptedMessage = encryptAES(str(client[0])+": "+message, client[2])
				client[1].send(reEncryptedMessage)

def readInKeys():
	global publicElGamalKeys
	global privateElGamalKey
	with open("id_elgamal.pub", "r") as publicKeyFile:
		publicElGamalKeys = publicKeyFile.read().split("\n")
	with open("id_elgamal", "r") as privateKeyFile:
		privateElGamalKey = int(privateKeyFile.read())

def exchangeSecret(connection):
	sendPublicKeys(connection)
	encryptedSecretC1 = int(connection.recv(BUFFERSIZE))
	encryptedSecretC2 = int(connection.recv(BUFFERSIZE))
	print "# done receiving secret"
	return decryptSharedSecret(encryptedSecretC1, encryptedSecretC2)

def sendPublicKeys(connection):
	connection.send("\n".join(publicElGamalKeys))
	connection.send("done")

def decryptSharedSecret(c1, c2):
	p = int(publicElGamalKeys[0])
	s = pow(c1, privateElGamalKey, p)
	message = c2 * modularInverse(s, p) % p
	return message

def encryptAES(message, key):
	return message

def decryptAES(message, key):
	return message


if __name__ == "__main__":
	sys.exit(main())