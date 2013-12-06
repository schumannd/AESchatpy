#!/usr/bin/python
import sys
import copy
from socket import socket
from numberTheory import *
import thread
from aes import *

clients = []
serverSocket = socket()
host = '127.0.0.1'
# hos = 'polaris.clarkson.edu'
port = 1233
BUFFERSIZE = 1024
moo = AESModeOfOperation()
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
	sharedSecretAsInteger = exchangeSecret(connection)
	# turn shared secret into byte array
	sharedSecret = [(sharedSecretAsInteger & (0xff << pos*8)) >> pos*8 for pos in range(32)]
	print "# done receiving secret"
	clients.append([address, connection, sharedSecret])
	sendReceiveLoop(connection, sharedSecret)

def sendReceiveLoop(connection, sharedSecret):
	while True:
		encryptedMessage = connection.recv(BUFFERSIZE)
		print "received cipher: ", encryptedMessage
		encryptedMessage = [ord(x) for x in list(encryptedMessage)]
		if not encryptedMessage: return
		message = decryptAES(encryptedMessage, sharedSecret)
		for client in clients:
			if connection != client[1]:
				reEncryptedMessage = encryptAES(str(client[0])+": "+message, client[2])
				client[1].send(''.join([chr(x) for x in reEncryptedMessage]))

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
	return decryptSharedSecret(encryptedSecretC1, encryptedSecretC2)

def sendPublicKeys(connection):
	connection.send("\n".join(publicElGamalKeys))
	connection.send("done")

def decryptSharedSecret(c1, c2):
	p = int(publicElGamalKeys[0])
	s = pow(c1, privateElGamalKey, p)
	message = c2 * modularInverse(s, p) % p
	return message

def encryptAES(cleartext, key):
	mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],
			key, moo.aes.keySize["SIZE_256"], key[:16])
	return ciph

def decryptAES(cipher, key):
	return moo.decrypt(cipher, None, moo.modeOfOperation["CFB"], key,
			moo.aes.keySize["SIZE_256"], key[:16])


if __name__ == "__main__":
	sys.exit(main())