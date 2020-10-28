import socket

import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import Transaction
hash = "SHA-256"


def newkeys(keysize):
    random_generator = Crypto.Random.get_random_bytes
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private


def importKey(externKey):
    return RSA.importKey(externKey)


def getpublickey(priv_key):
    return priv_key.publickey()


def crypt(message, pub_key):
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)


def decrypt(ciphertext, priv_key):
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)


def sign(message, priv_key, hashAlg="SHA-256"):
    global hash
    hash = hashAlg
    signer = PKCS1_v1_5.new(priv_key)

    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)


def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)


def register():
    print("The registration is completed!")
    public, private = newkeys(2048)
    # print("Your public key is:")
    # print(public.exportKey().decode())
    print("Your private key is:")
    key = [str(private.n), str(private.e), str(private.d)]
    print(str(private.n) + " " + str(private.e) + " " + str(private.d))
    print("Save your private key or you will not be able to access your wallet again!")
    return public, private


def login(key):
    k = key.split()
    for i in range(len(k)):
        k[i] = int(k[i])
    check_key = RSA.construct(k, consistency_check=True)
    print(check_key.n)
    return check_key.publickey(), check_key


def send_money(private_key, sender):
    print("Insert the public key or the receiver:")
    receiver = input()
    print("Insert the amount of money you want to send:")
    amount = input()
    # TODO check input data
    #new_transaction = Transaction(sender, receiver, amount)
    new_transaction="pippo"
    sign_of_transaction = sign(new_transaction.encode(), private_key, "SHA256")
    packet_to_send = [new_transaction, sign_of_transaction]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto(packet_to_send, ("224.0.0.0", 2000))

def verify_transaction(transaction: Transaction):
    public = transaction[0].sender
    return verify(transaction[0], transaction[1], public)
