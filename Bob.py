# Maddie Zug
# A2
# Bob is a server that listens for messages from Mallory

import socket
import sys
import argparse
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import unpad
from Crypto.Hash import CMAC
import datetime
import pickle

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

# Bind the socket to the address given on the command line
server_name = args.servername
port_num = args.portnum
server_address = (server_name, port_num)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

# Load private key
private_key_bob = RSA.import_key(open("private_key_bob.pem").read())

# Get timestamp
timestamp = datetime.datetime.now()

message_count = 0
handshake = 1

while True:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('client connected:', client_address)
        while True:
            data = connection.recv(1024)
            if handshake:
                print("Received handshake. Verifying now.")
                try:
                    (timestamp_alice, enc_session_key, signature) = pickle.loads(data)
                    timestamp_alice = timestamp_alice[1:27]
                    timestamp_alice = datetime.datetime.strptime(timestamp_alice, "%Y-%m-%d %H:%M:%S.%f")
                    time_difference = timestamp_alice-timestamp
                    if(time_difference.seconds > 120):
                        print("Uh oh, timestamp on the handshake is invalid!")
                        connection.close()
                    cipher_rsa = PKCS1_OAEP.new(private_key_bob)
                    session_key = cipher_rsa.decrypt(enc_session_key)[1:]
                    print("session key: ", session_key)
                    #h = SHA.new(data)
                    #try:
                    #     pkcs1_15.new(public_key_alice).verify(h, signature):
                    #     print "The signature is valid."
                    # except (ValueError, TypeError):
                    #     print "The signature is not valid."
                    #     connection.close()
                    handshake = 0
                except: 
                    print("Invalid handshake")
                    connection.close()
            elif data:
                (message_num, data) = pickle.loads(data)
                print("***********************************")
                print("Message number: ", message_num)
                print("Received: ", data)
                if(message_num != message_count):
                    print("Message numbers don't align! Mallory messed with messages!")
                message_count = message_count + 1
                ################### ENC + MAC MODE ######################
                if(args.enc and args.mac):
                    try:
                        (ct, iv, tag) = pickle.loads(data)
                        cipher = AES.new(session_key, AES.MODE_CBC, iv)
                        message = unpad(cipher.decrypt(ct), AES.block_size)
                        print("Message: ", message)
                        cobj = CMAC.new(session_key, ciphermod=AES)
                        cobj.update(message)
                        try:
                            cobj.verify(tag)
                            print("The message is authentic")
                        except ValueError:
                            print("The message or the key is wrong")
                    except:
                        Print("Mallory tried to modify the message!")
                ################### ENC MODE ######################
                elif (args.enc):
                    # Decrypt the data with the AES session key
                    try:
                        (ct, iv) = pickle.loads(data)
                        cipher = AES.new(session_key, AES.MODE_CBC, iv)
                        message = unpad(cipher.decrypt(ct), AES.block_size)
                        print("Message: ", message)
                    except:
                        print("Mallory tried to modify the message!")
                ################### MAC MODE ######################
                elif (args.mac):
                    try:
                        (message, tag) = pickle.loads(data)
                        print("Message: ", message)
                        cobj = CMAC.new(session_key, ciphermod=AES)
                        cobj.update(message)
                        try:
                            cobj.verify(tag)
                            print("The message is authentic")
                        except ValueError:
                            print("The message or the key is wrong")
                    except:
                        print("Warning- Mallory tried to modify the message!")
                ################### UNSAFE MODE ######################
                # Just print, done above


    finally:
        connection.close()