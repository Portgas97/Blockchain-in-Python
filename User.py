import socket
import struct
import Crypto
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from Crypto.Util import number
from Transaction import Transaction
import json
import BlockChain
from BlockChain import local_blockchain
from Block import Block
import hashlib
import time
import base64
from ServerListener import ServerThreadListener

hash = "SHA-256"
public_key = 0
private_key = 0
buffer = " "

###############################################################################
#                    FUNZIONI CRITTOGRAFICHE DI UTILITÀ                       #
###############################################################################

def newkeys(keysize):
    global public_key
    global private_key

    random_generator = Crypto.Random.get_random_bytes
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()

    public_key = public
    private_key = private

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
def verify(message, signature, pub_key,hash="SHA-256"):
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


###############################################################################
#                          FUNZIONI PER L'UTENTE
##############################################################################

def register():
    print("The registration is completed!\n")
    public, private = newkeys(2048)
    print("Your public key is:\n")
    print(str(public.n) + "_" + str(public.e) + "\n")
    print("Your private key is:\n")
    key = [str(private.n), str(private.e), str(private.d)]
    print(str(private.n) + " " + str(private.e) + " " + str(private.d) + "\n")
    print("Save your private key or you will not be able to access your wallet again!\n")
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
    print("Transazione di: " + amount + " DSSCoin verso: " + receiver + "\n")

    tmp = receiver.split("_")
    n = int(tmp[0])
    e = int(tmp[1])

    #check sender != receiver

    if sender.n == n and sender.e == e:
        print("Sender is uqual to Receiver")
        return

    #check amount of money

    if local_blockchain.count_money(sender)<int(amount):
        print("Not enough money")
        return

    receiver_public_key = RSA.construct([n, e])


    packet = {
        "sender_n": sender.n,
        "sender_e": sender.e,
        "amount": amount,
        "receiver_n": receiver_public_key.n,
        "receiver_e": receiver_public_key.e,
        "timestamp": time.time()
    }
    #message_to_send = json.dumps(packet)
    sign_of_transaction = sign(packet.__str__().encode(), private_key, "SHA-256")
    new_transaction = Transaction(sender, amount, receiver_public_key,f"{sign_of_transaction}", packet["timestamp"])
    #packet["sign"]=sign_of_transaction
    #packet["sign"]=number.bytes_to_long(sign_of_transaction)
    packet["sign"]=f"{sign_of_transaction}"
    print("chiave generata")
    print(sign_of_transaction)
    message_to_send = json.dumps(packet)
    #print("Messaggio user (sign_of_transaction):")
    #print(sign_of_transaction)

    # creazione del socket per trasmettere, invio della transazione in formato JSON, firma appesa in seguito
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    # divisore per fare la split lato ricevente
    #print("DEBUG_LOG: chiamata a send_to() dentro a send_money()")
    sock.sendto((message_to_send).encode(), ("224.0.0.0", 2000))



def exists_blockchain():
    server_listener = ServerThreadListener()
    server_listener.start()
    #print("DEBUG_LOG: chiamata a exists_blockchain()")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    #sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    #sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock1.bind(('', 2001))
    #mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)
    #sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    sock.sendto("exists".encode(), ("224.0.0.0", 2000))


    try:
        server_listener.join(timeout=1)

    except:
        #print("DEBUG_LOG: terminazione exists_blockchain, valore di ritorno: False, causa: recv scaduta\n")
        return False

    if buffer == "False":
        #print("DEBUG_LOG: terminazione exists_blockchain, valore di ritorno: False, causa: valore di ritorno == False\n")
        return False

    if buffer == "True":
        #print("DEBUG_LOG: terminazione exists_blockchain, valore di ritorno: True, causa: valore di ritorno == True\n")
        return True



def update_blockchain():
    global public_key

    server_listener = ServerThreadListener()
    server_listener.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    if not local_blockchain.last_block():
        # lo spazio dopo update serve come divisore in Listener.py
        sock.sendto("update ".encode() + "empty ".encode()+ str(public_key.n).encode() + "_".encode() + str(public_key.e).encode(), ("224.0.0.0", 2000))
    else:
        # lo spazio dopo update serve come divisore in Listener.py
        sock.sendto("update ".encode() + str(BlockChain.local_blockchain.last_block().index).encode()+ " ".encode() + str(public_key.n).encode() + "_".encode() + str(public_key.e).encode(), ("224.0.0.0", 2000))
    try:
        server_listener.join(1)
    except:
        print("timeout")
        return False

    update=buffer

    if update == "index_error":
        print("Wrong index")
        return

    if update == "Already up to date":
        print(update)
        return

    else:
        # print("DEBUG_JSON_ARRIVED "+update)
        try:
            dict = json.loads(update)
        except:
            print("An error occurs, i'm retrying.")
            return update_blockchain()

        blocks=[]
        # print("DEBUG_UPDATE"+"".join(dict))
        for i in dict:
            i_dict=dict[i]
            i_index=i_dict['index']
            i_transactions=i_dict['transactions']
            i_nonce=i_dict['nonce']
            i_previous_hash=i_dict['previous_hash']
            i_timestamp=i_dict['timestamp']
            transactions=[]

            for j in i_transactions:
                tmp=i_transactions[j]
                tmp_sender=tmp['sender']
                tmp_amount=tmp['amount']
                tmp_receiver=tmp['receiver']
                tmp_timestamp=tmp['timestamp']
                tmp_sign=tmp['sign']
                new_transaction=Transaction(tmp_sender,tmp_amount,tmp_receiver,eval(tmp_sign),tmp_timestamp)
                transactions.append(new_transaction)
                
            new_block=Block(i_index,transactions,i_nonce,i_previous_hash,i_timestamp)
            local_blockchain.add_block(new_block)


def verify_transaction(transaction: Transaction):
    public = transaction[0].sender
    return verify(transaction[0], transaction[1], public)
