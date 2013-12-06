#!/usr/bin/python 
import sys
import random
from socket import socket
import thread
from aes import *


davidsSocket = socket()
host = '127.0.0.1'
# host = 'polaris.clarkson.edu'
port = 1233
BUFFERSIZE = 1024
moo = AESModeOfOperation()
# create key and turn it into byte array
sharedSecretAsInteger = random.getrandbits(256)
sharedSecret = [int(sharedSecretAsInteger & (0xff << pos*8)) >> pos*8 for pos in range(32)]

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
		davidsSocket.send(''.join([chr(x) for x in cipher]))
	davidsSocket.close

def exchangeSecret():
	publicKeys = recievePublicKeys()
	encryptedSharedSecret = encryptSharedSecretWithElGamal(int(publicKeys[0]),
		int(publicKeys[1]), int(publicKeys[2]))
	print "# sending shared secret..."
	davidsSocket.send(str(encryptedSharedSecret[0]))
	davidsSocket.send(str(encryptedSharedSecret[1]))
	print "# ...done"
	return

def recievePublicKeys():
	publicKeys = ""
	incomingMessage = "start"
	print "# receiving public keys"
	while incomingMessage != "done":
		incomingMessage = davidsSocket.recv(BUFFERSIZE)
		publicKeys += incomingMessage
	print "# ...done"
	return publicKeys[:-5].split("\n")

def encryptSharedSecretWithElGamal(p, g, b):
	y = random.randrange(1, p-1)
	c1 = pow(g, y, p)
	s = pow(b, y, p)
	c2 = (sharedSecretAsInteger*s)%p
	return [c1, c2]

def encrypt(cleartext):
	mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CFB"],
			sharedSecret, moo.aes.keySize["SIZE_256"], sharedSecret[:16])
	return ciph

def decrypt(cipher):
	return moo.decrypt(cipher, None, moo.modeOfOperation["CFB"], sharedSecret,
			moo.aes.keySize["SIZE_256"], sharedSecret[:16])

def recieve(connection):
	while True:
		cipher = connection.recv(BUFFERSIZE)
		message = decrypt([ord(x) for x in list(cipher)])
		print message

if __name__ == "__main__":
	sys.exit(main())
