AESchatpy
=========

Chat program that is secured by the AES standard

Key exchange is done via ElGamal using existing key files

Creation of these files can be seen in my other tools

public key file:
p		large prime for cyclic Group G
g		generator for Group G
b		public key = g^a mod p

private key file:
a		private random exponent

Th AES implementation (aes.py) has been taken from:
http://anh.cs.luc.edu/331/code/aes.py

