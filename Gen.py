import Crypto
from Crypto.PublicKey import RSA

#Alice's private key
key = RSA.generate(2048)
private_key_alice = key.export_key()
file_out = open("private_key_alice.pem", "wb")
file_out.write(private_key_alice)
print("Alice's private key: ", private_key_alice)

#Alice's public key
public_key_alice = key.publickey().export_key()
file_out = open("public_key_alice.pem", "wb")
file_out.write(public_key_alice)
print("Alice's public key: ", public_key_alice)

#Bob's private key
key = RSA.generate(2048)
private_key_bob = key.export_key()
file_out = open("private_key_bob.pem", "wb")
file_out.write(private_key_bob)
print("Bob's private key: ", private_key_bob)

#Bob's public key
public_key_bob = key.publickey().export_key()
file_out = open("public_key_bob.pem", "wb")
file_out.write(public_key_bob)
print("Bob's public key: ", public_key_bob)