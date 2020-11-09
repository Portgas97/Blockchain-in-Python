import time
from threading import Thread

import socket
import struct
from Crypto.PublicKey import RSA
import User
import json
import BlockChain
import Block
from BlockChain import local_blockchain
import hashlib

update2 = 0


class ServerThreadListener(Thread):

    # metodo che rappresenta le attività compiute dal thread
    def run(self):
        # creazione del socket, utilizza IPv4, di tipo UDP
        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # SO_REUSEADDR è u flag che dice al kernel di riusare un socket locale nello stato 'TIME_WAIT', senza aspettare per il timeout
        # level = SOL_SOCKET implica che manipoliamo a livello di API
        sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock1.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # '' equivale a INADDR_ANY, si fa il bind su tutte le interfacce
        sock1.bind(('', 2001))

        # funzione che converte i valori passati in un bytes object secondo le modalità espresse da format
        # s = char (4s significa 4 byte), l = long, = native byte order + standard size and alignment
        # 224.0.0.0 è uno degli indirizzi adibiti al multicast
        mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)

        # aggiungiamo al multicast group
        sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            global update2
            print("DEBUG_LOG: Listener torna ad eseguire while true, ascolto...")
            # dimensione del buffer
            update2 = sock1.recv(10240).decode()

            print("update")
