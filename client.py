#!/usr/bin/python 
import sys
import random
from socket import socket
import thread

davidsSocket = socket()
host = '127.0.0.1'
port = 1234
BUFFERSIZE = 1024
sharedSecret = random.getrandbits(256)

def main():
	davidsSocket.connect((host,port))
	exchangeSecret()
	# new thread for receiving
	thread.start_new_thread(recieve, (davidsSocket,))
	# use this thread for sending
	while True:
		message = raw_input()
		if not message: break
		cipher = encrypt(message)
		davidsSocket.send(cipher)
	davidsSocket.close

def recievePublicKeys():
	publicKeys = ""
	incomingMessage = "start"
	print "receiving public keys"
	while incomingMessage != "done":
		incomingMessage = davidsSocket.recv(BUFFERSIZE)
		publicKeys += incomingMessage
	print "...done"
	return publicKeys[:-5].split("\n")

def exchangeSecret():
	publicKeys = recievePublicKeys()
	encryptedSharedSecret = encryptSharedSecretWithElGamal(int(publicKeys[0]),
		int(publicKeys[1]), int(publicKeys[2]))
	print "sending shared secret..."
	davidsSocket.send(str(encryptedSharedSecret[0]))
	davidsSocket.send(str(encryptedSharedSecret[1]))
	print "...done"
	return

def encryptSharedSecretWithElGamal(p, g, b):
	y = random.randrange(1, p-1)
	c1 = pow(g, y, p)
	s = pow(b, y, p)
	c2 = (sharedSecret*s)%p
	return [c1, c2]

def encrypt(message):
	return message

def decrypt(message):
	return message

def recieve(connection):
	while True:
		cipher = connection.recv(BUFFERSIZE)
		message = decrypt(cipher)
		print message

if __name__ == "__main__":
	sys.exit(main())