# Maddie Zug
# A2

import socket
import sys
import argparse
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import datetime
import pickle

# Take server names and ports of bob and alice as command line args
parser = argparse.ArgumentParser()
parser.add_argument("servername_bob", 
                    help="Name of Bob's server to connect to.")
parser.add_argument("portnum_bob", type=int,
                    help="Bob's port number to connect to.")
parser.add_argument("servername_alice", 
                    help="Name of Alice's server to connect to.")
parser.add_argument("portnum_alice", type=int,
                    help="Alice's port number to connect to.")
args = parser.parse_args()

# Create a TCP/IP socket
socket_bob = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_alice = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set up addressing for bob's server and port
server_name_bob = args.servername_bob
port_num_bob = args.portnum_bob
server_address_bob = (server_name_bob, port_num_bob)

#Set up addressing for Alice's server and port
server_name_alice = args.servername_alice
port_num_alice = args.portnum_alice
server_address_alice = (server_name_alice, port_num_alice)

# Bind to Alice's address to look for messages
socket_alice.bind(server_address_alice)
socket_alice.listen(1)

# Load public keys
public_key_bob = RSA.import_key(open("public_key_bob.pem").read())
public_key_alice = RSA.import_key(open("public_key_alice.pem").read())

# Get timestamp
timestamp = datetime.datetime.now()

#
message_dict = {}

handshake = 1;

while True:
    print('waiting for a connection')
    connection, client_address = socket_alice.accept()
    try:
        print('client connected:', client_address)
        
        # Connect to bob's server to be able to send him messages
        print('connecting to %s port %s' % server_address_bob)
        socket_bob.connect(server_address_bob)

        # Receive data and forward, modify, repeat, or replay
        while True:
            data = connection.recv(1024)
            if(handshake):
                print("Received handshake. Forwarding now.")
                socket_bob.sendall(data)
                handshake = 0
            else:
                print('received "%s"' % data)
                (message_num, message_contents) = pickle.loads(data)
                message_dict[message_num] = message_contents
                if data:
                    action = input("What would you like to do?\n Type d to delete, m to modify, r to replay, return to send as is:")
                    if (action == "d"):
                        print("Deleted message")
                    elif(action == "m"):
                        new_message = input("Type new message: ")
                        bytes_to_send = pickle.dumps((message_num, new_message.encode('UTF-8')))
                        socket_bob.sendall(bytes_to_send)
                        print("Modified message sent to Bob")
                    elif(action == "r"):
                        message_num_input = input("Enter message number to replay: ")
                        message = message_dict[int(message_num_input)]
                        bytes_to_send = pickle.dumps((message_num, message))
                        socket_bob.sendall(bytes_to_send)
                        print("Replayed message sent to Bob")
                    else:
                        socket_bob.sendall(data)
                        print("Message sent to Bob without modification")
                else:
                    break
    finally:
        connection.close()
        socket_alice.close()
        socket_bob.close()