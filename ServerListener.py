import time
from threading import Thread, RLock

import socket
import struct
from Crypto.PublicKey import RSA
import User
import json
import BlockChain
from Block import Block
from BlockChain import local_blockchain
import hashlib
from Transaction import Transaction
mutex = RLock()

def set_buffer(tmp: str):
    User.buffer = tmp

def validate_proof_of_work(block):
    str_to_hash=""
    for i in range(0, len(block.transactions)):
        str_to_hash+=block.transactions[i].sender + str(block.transactions[i].amount) + \
                                      block.transactions[i].receiver + str(block.transactions[i].timestamp)

    str_to_hash += local_blockchain.last_block().block_hash + str(block.nonce)

    first_hash_256 = hashlib.sha256(str_to_hash.encode()).hexdigest()
    second_hash_256 = hashlib.sha256(first_hash_256.encode()).hexdigest()

    if second_hash_256[:local_blockchain.difficulty] == local_blockchain.difficulty*"0":
        return True
    else:
        return False


class ServerThreadListener(Thread):

    # metodo che rappresenta le attività compiute dal thread
    def run(self):
        # creazione del socket, utilizza IPv4, di tipo UDP
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # SO_REUSEADDR è u flag che dice al kernel di riusare un socket locale nello stato 'TIME_WAIT', senza aspettare per il timeout
        # level = SOL_SOCKET implica che manipoliamo a livello di API
        sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # '' equivale a INADDR_ANY, si fa il bind su tutte le interfacce
        sock1.bind(('', 2001))

        # funzione che converte i valori passati in un bytes object secondo le modalità espresse da format
        # s = char (4s significa 4 byte), l = long, = native byte order + standard size and alignment
        # 224.0.0.0 è uno degli indirizzi adibiti al multicast
        mreq1 = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)

        # aggiungiamo al multicast group
        sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq1)

        # print("DEBUG_LOG: Listener torna ad eseguire while true, ascolto...")
        buffer = sock1.recv(2**16).decode()
        # print("RICEVUTO:"+ buffer)
        set_buffer(buffer)
        # print(User.buffer)


class BlockListener(Thread):
    print("ciao")

    def run(self):
        # creazione del socket, utilizza IPv4, di tipo UDP
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # SO_REUSEADDR è u flag che dice al kernel di riusare un socket locale nello stato 'TIME_WAIT', senza aspettare per il timeout
        # level = SOL_SOCKET implica che manipoliamo a livello di API
        sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # '' equivale a INADDR_ANY, si fa il bind su tutte le interfacce
        sock1.bind(('', 2002))

        # funzione che converte i valori passati in un bytes object secondo le modalità espresse da format
        # s = char (4s significa 4 byte), l = long, = native byte order + standard size and alignment
        # 224.0.0.0 è uno degli indirizzi adibiti al multicast
        mreq1 = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)

        # aggiungiamo al multicast group
        sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq1)

        # print("DEBUG_LOG: Listener torna ad eseguire while true, ascolto...")
        while True:
            buffer = sock1.recv(10240).decode()
            block_received=json.loads(buffer)
            print("BLOCK LISTENER")
            print("block listener: " + buffer)
            if buffer == "":
                print("il buffer è vuoto")
                continue
            i_index = block_received['index']
            i_transactions = block_received['transactions']
            i_nonce = block_received['nonce']
            i_previous_hash = block_received['previous_hash']
            i_timestamp = block_received['timestamp']
            transactions = []
            for j in i_transactions:
                tmp = i_transactions[j]
                tmp_sender = tmp['sender']
                tmp_amount = tmp['amount']
                tmp_receiver = tmp['receiver']
                tmp_timestamp = tmp['timestamp']
                tmp_sign = tmp['sign']
                new_transaction = Transaction(tmp_sender, tmp_amount, tmp_receiver, eval(tmp_sign), tmp_timestamp)
                transactions.append(new_transaction)


            if i_transactions["2"]["receiver"]==str(User.public_key.n)+"_"+str(User.public_key.e):
                print("non rispondo a me stesso")
                continue

            new_block = Block(i_index, transactions, i_nonce, i_previous_hash, i_timestamp)

            print("validate proof of work: " + str(validate_proof_of_work(new_block)))

            block_interested = None

            try:
                block_interested=local_blockchain.get_chain()[new_block.index]
            except:
                print("Il blocco non esiste")
                if validate_proof_of_work(new_block):
                    local_blockchain.add_block(new_block)
                    continue

            if block_interested is not None and new_block.timestamp < block_interested.timestamp:
                local_blockchain.remove_tail(new_block.index)
                print("DEBUG BLOCK LISTENER")
                print(local_blockchain.add_block(new_block))

