from BlockChain import local_blockchain
from Transaction import Transaction
from threading import Thread, RLock
from Crypto.PublicKey import RSA
from Block import Block
import BlockChain
import hashlib
import socket
import struct
import User
import time
import json

mutex = RLock()

def set_buffer(tmp: str):
    User.buffer = tmp


class ServerThreadListener(Thread):

    # metodo che rappresenta le attività compiute dal thread
    def run(self):
        mutex.acquire()
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
        buffer = sock1.recv(10240).decode()
        # print("RICEVUTO:"+ buffer)
        set_buffer(buffer)
        mutex.release()
        # print(User.buffer)


class BlockListener(Thread):

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
        buffer = sock1.recv(10240).decode()

        block_received=json.loads(buffer)

        # print("BLOCK LISTENER")
        # print(buffer)
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

        new_block = Block(i_index, transactions, i_nonce, i_previous_hash, i_timestamp)

        try:
            block_interested=local_blockchain.get_chain()[new_block.index]
        except:
            print("The block does not exists alreay, adding block to the Blockchain")
            local_blockchain.add_block(new_block)
            return

        if new_block.timestamp < block_interested.timestamp:
            local_blockchain.remove_tail(new_block.index)
            print("DEBUG BLOCK LISTENER")
            print(local_blockchain.add_block(new_block))
