import socket
import struct
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from Transaction import Transaction
import json
import BlockChain
from BlockChain import local_blockchain
from Block import Block
import time

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


# verifica la validità della firma
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
    print("Your public key is:")
    print(str(public.n) + "_" + str(public.e))
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


def send_money(private_key: Crypto.PublicKey.RSA.RsaKey, sender):
    print("Insert the public key or the receiver:")
    receiver = input()
    print("Insert the amount of money you want to send:")
    amount = input()
    # TODO check input data
    # chiave pubblica del destinatario
    tmp = receiver.split("_")
    n = int(tmp[0])
    e = int(tmp[1])
    receiver_public_key = RSA.construct([n, e])
    new_transaction = Transaction(sender, amount, receiver_public_key)
    packet = {
        "sender_n": new_transaction.sender.n,
        "sender_e": new_transaction.sender.e,
        "amount": new_transaction.amount,
        "receiver_n": new_transaction.receiver.n,
        "receiver_e": new_transaction.receiver.e,
        "timestamp": new_transaction.timestamp
    }
    message_to_send = json.dumps(packet)
    sign_of_transaction = sign(packet.__str__().encode(), private_key, "SHA256")
    print("messaggio user")
    print(sign_of_transaction)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.sendto((message_to_send + "divisore").encode() + sign_of_transaction, ("224.0.0.0", 2000))


def verify_transaction(transaction: Transaction):
    public = transaction[0].sender
    return verify(transaction[0], transaction[1], public)


def exists_blockchain():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind(('', 2001))
    mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)
    sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sock.sendto("exists".encode(), ("224.0.0.0", 2000))

    sock1.settimeout(1)
    # dimensione del buffer
    try:
        exists = sock1.recv(10240)
    except:
        return False
    if exists.decode() == "False":
        return False
    if exists.decode() == "True":
        return True


def update_blockchain():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    if not local_blockchain.last_block():
        sock.sendto("update ".encode() + "empty".encode(), ("224.0.0.0", 2000))
    else:
        sock.sendto("update ".encode() + str(BlockChain.local_blockchain.last_block().index).encode(), ("224.0.0.0", 2000))
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind(('', 2001))
    mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)
    sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sock1.settimeout(1)
    # dimensione del buffer
    update = sock1.recv(10240)
    if update == "index_error":
        print("Wrong index")
        return
    if update == "Already up to date":
        print(update)
        return
    else:
        update.decode()
        dict = json.loads(update)
        blocks=[]
        for i in dict:
            i_dict=dict[i]
            i_index=i_dict['index']
            i_transactions=i_dict['transactions']
            i_nonce=i_dict['nonce']
            i_previous_hash=i_dict['previous_hash']
            i_timestamp=i_dict['timestamp']
            new_block=Block(i_index,i_transactions,i_nonce,i_previous_hash,i_timestamp)
            local_blockchain.add_block(new_block)