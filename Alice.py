# Maddie Zug
# A2

import socket
import sys
import argparse
import Crypto
import hashlib
import base64
from base64 import b64encode
import os
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Hash import CMAC
import datetime
import pickle


# Set up with Mallory's server and port as command line args
parser = argparse.ArgumentParser()
parser.add_argument("servername", 
                    help="Name of server to connect to.")
parser.add_argument("portnum", type=int,
                    help="Port number to connect to.")
parser.add_argument("--enc", help="Encryption mode. All messages will be sent encrypted.", action="store_true")
parser.add_argument("--mac", help="Mac mode. All messages will be sent with an identifier.", action="store_true")

args = parser.parse_args()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server specified
server_name = args.servername
port_num = args.portnum
server_address = (server_name, port_num)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

# Message number/identifier
message_num = 0

# Load and generate keys
public_key_bob = RSA.import_key(open("public_key_bob.pem").read())
private_key_alice = RSA.import_key(open("private_key_alice.pem").read())
session_key = get_random_bytes(16)
print("session_key: ", session_key)

# Get timestamp
timestamp = datetime.datetime.now()

# Construct first handshake message
cipher_rsa = PKCS1_OAEP.new(public_key_bob)
enc_session_key = cipher_rsa.encrypt("A".encode()+session_key)
to_be_signed_message = "B".encode()+str(timestamp).encode()+enc_session_key
h = SHA256.new(to_be_signed_message)
signature = pkcs1_15.new(private_key_alice).sign(h)
handshake = ("B"+str(timestamp),enc_session_key,signature)
#handshake = "B".encode()+str(timestamp).encode()+enc_session_key+signature
handshake_bytes = pickle.dumps(handshake)
sock.sendall(handshake_bytes)

try:
    while(True):
        # Ask user for message
        message = input("Enter a message: ")

        ################### ENC + MAC MODE ######################
        if(args.enc and args.mac):
            # Encrypt the data with the AES session key
            cipher = AES.new(session_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
            iv = cipher.iv
            #generate the MAC
            cobj = CMAC.new(session_key, ciphermod=AES)
            cobj.update(message.encode('UTF-8'))
            tag = cobj.digest()
            # Send a tuple to make it easy to unpack data on the other end
            bytes_to_send = pickle.dumps((ct_bytes, iv, tag))
            bytes_to_send = pickle.dumps((message_num, bytes_to_send))
        ################### ENC MODE ######################
        elif (args.enc):
            # Encrypt the data with the AES session key
            cipher = AES.new(session_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
            iv = cipher.iv
            # Send a tuple to make it easy to unpack data on the other end
            bytes_to_send = pickle.dumps((ct_bytes, iv))
            bytes_to_send = pickle.dumps((message_num, bytes_to_send))
        ################### MAC MODE ######################
        elif (args.mac):
            cobj = CMAC.new(session_key, ciphermod=AES)
            cobj.update(message.encode('UTF-8'))
            tag = cobj.digest()
            tagged_message = (message.encode('UTF-8'), tag)
            tagged_message_bytes = pickle.dumps(tagged_message)
            bytes_to_send = pickle.dumps((message_num, tagged_message_bytes))
        else:
            print('sending "%s"' % message)
            bytes_to_send = pickle.dumps((message_num, message.encode('UTF-8')))
            
        
        sock.sendall(bytes_to_send)
        message_num = message_num + 1

finally:
    sock.close()