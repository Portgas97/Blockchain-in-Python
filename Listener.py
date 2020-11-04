from threading import Thread

import socket
import struct
from Crypto.PublicKey import RSA
import User
import json
import BlockChain
from BlockChain import local_blockchain

class ThreadListener(Thread):
    #metodo che rappresenta le attività compiute dal thread
    def run(self):
        # creazione del socket, utilizza IPv4, di tipo UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # SO_REUSEADDR è u flag che dice al kernel di riusare un socket locale nello stato 'TIME_WAIT', senza aspettare per il timeout
        # level = SOL_SOCKET implica che manipoliamo a livello di API
        # SO_REUSEADDR dice al kernel di riusare indirizzi locali se sono nello stato di TIME_WAIT anche prima della scadenza del timeout
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock1.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        # '' equivale a INADDR_ANY, si fa il bind su tutte le interfacce. (host, port)
        sock.bind(('', 2000))
        # funzione che converte i valori passati in un bytes object secondo le modalità espresse da format (primo parametro).
        # s = char (4s significa 4 byte), l = long, = native byte order + standard size and alignment
        # ascoltiamo su tutte le interfacce
        # 224.0.0.0 è uno degli indirizzi adibiti al multicast
        mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)
        # aggiungiamo al multicast group
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        while True:
            recv=sock.recv(10240) # infatti non si usa recvfrom per multicasting
            if recv.decode()=="exists":
                print("blockchain:" + "".join(str(local_blockchain.get_chain())))
                if not local_blockchain.get_chain():
                    sock1.sendto("False".encode(), ("224.0.0.0", 2001))
                    print("listener:" + "false")
                if local_blockchain.get_chain():
                    sock1.sendto("True".encode(), ("224.0.0.0", 2001))
                    print("listener:" + "true")

            elif recv.decode()[:6]=="update":
                    tmp = recv.decode().split(" ")
                    last_block=tmp[1]
                    if last_block == "empty":
                        json_blocks = {}
                        index=BlockChain.local_blockchain.last_block().index
                        dict = {i: local_blockchain.get_chain()[i] for i in range(0, index+1)}
                        print("index: " + str(index))
                        json_blocks=json.dumps(dict)
                        #for i in range[:index]:
                        #    new_block = {}
                        #    new_block[i] = BlockChain.local_blockchain.full_chain()[i]
                        #    json_blocks = json.dumps(new_block)
                        print("dict: "+"".join(dict))
                        sock1.sendto(json_blocks.encode(), ("224.0.0.0", 2001))

                    elif int(last_block) == BlockChain.local_blockchain.last_block().index:
                        sock1.sendto("Already up to date".encode(), ("224.0.0.0", 2001))
                    elif int(last_block) < BlockChain.local_blockchain.last_block().index:
                        #blockchain_to_send=BlockChain.full_chain()[last_block:-1]
                        json_blocks={}

                        for i in range[last_block:BlockChain.local_blockchain.last_block().index]:
                            new_block = {}
                            new_block[i] = BlockChain.local_blockchain.get_chain()[i]
                            json_blocks = json.dumps(new_block)
                        sock1.sendto(json_blocks.encode(), ("224.0.0.0", 2001))
                    elif int(last_block) > BlockChain.local_blockchain.last_block().index:
                        print("Index not valid")
                        sock1.sendto("index_error".encode(), ("224.0.0.0", 2001))
            else:
                message_arrived=recv.split(b'divisore')
                sign=message_arrived[1]
                message=json.loads(message_arrived[0])
                print(message)
                message_sender_n=message["sender_n"]
                message_sender_e=message["sender_e"]
                sender_key = RSA.construct([message_sender_n, message_sender_e])
                is_valid=User.verify(message.__str__().encode(),sign, sender_key)
                print("messaggio listener")
                print(sign)
                print("Transiction is valid:"+str(is_valid))


    # TODO Mining
