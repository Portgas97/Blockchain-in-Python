
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

class ThreadListener(Thread):

    # metodo che rappresenta le attività compiute dal thread
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

        #count transactions
        number_of_transactions=0
        while True:

            recv = sock.recv(10240)  # infatti non si usa recvfrom per multicasting
            msg=""
            try:
                msg=recv.decode()
            except:
                print(msg)

            if msg == "exists":
                if not local_blockchain.get_chain():
                    sock1.sendto("False".encode(), ("224.0.0.0", 2001))
                if local_blockchain.get_chain():
                    sock1.sendto("True".encode(), ("224.0.0.0", 2001))

            elif msg[:6] == "update":
                tmp = recv.decode().split(" ")
                last_block = tmp[1]
                if last_block == "empty":
                    index = BlockChain.local_blockchain.last_block().index
                    packets = []
                    for i in range(0, index + 1):
                        new_block = local_blockchain.get_chain()[i]
                        transactions=new_block.transactions
                        dict_tra=[]
                        for j in range (0, len(transactions)):
                            new_dict = {
                                "sender": transactions[j].sender,
                                "amount": transactions[j].amount,
                                "receiver": transactions[j].receiver,
                                "timestamp": transactions[j].timestamp,
                            }
                            dict_tra.append(new_dict)
                            dict_transactions = {i: dict_tra[i] for i in range(0, len(transactions))}
                        new_packet = {
                            "index": new_block.index,
                            "transactions": dict_transactions,
                            "nonce": new_block.nonce,
                            "previous_hash": new_block.previous_hash,
                            "timestamp": new_block.timestamp
                        }
                        packets.append(new_packet)

                    dict = {i: packets[i] for i in range(0, index + 1)}
                    json_packet = json.dumps(dict)
                    sock1.sendto(json_packet.encode(), ("224.0.0.0", 2001))

                elif int(last_block) == BlockChain.local_blockchain.last_block().index:
                    sock1.sendto("Already up to date".encode(), ("224.0.0.0", 2001))

                elif int(last_block) < BlockChain.local_blockchain.last_block().index:
                    index = BlockChain.local_blockchain.last_block().index
                    packets = []
                    for i in range(int(last_block), index + 1):
                        new_block = local_blockchain.get_chain()[i]
                        new_packet = {
                            "index": new_block.index,
                            "transactions": new_block.transactions,
                            "nonce": new_block.nonce,
                            "previous_hash": new_block.previous_hash,
                            "timestamp": new_block.timestamp
                        }
                        packets.append(new_packet)

                    dict = {i: packets[i] for i in range(int(last_block), index + 1)}
                    json_packet = json.dumps(dict)
                    print(json_packet)
                    sock1.sendto(json_packet.encode(), ("224.0.0.0", 2001))

                elif int(last_block) > BlockChain.local_blockchain.last_block().index:
                    print("Index not valid")
                    sock1.sendto("index_error".encode(), ("224.0.0.0", 2001))
            else:

                message_arrived = recv.split(b'divisore')
                sign = message_arrived[1]
                message = json.loads(message_arrived[0])
                print(message)
                message_sender_n = message["sender_n"]
                message_sender_e = message["sender_e"]
                message_amount=message["amount"]
                message_receiver_n = message["receiver_n"]
                message_reveicer_e = message["receiver_e"]
                message_timestamp=message["timestamp"]
                sender_key = RSA.construct([message_sender_n, message_sender_e])
                is_valid = User.verify(message.__str__().encode(), sign, sender_key)
                print("messaggio listener")
                print(sign)
                print("Transiction is valid:" + str(is_valid))
                number_of_transactions=number_of_transactions+1
                local_blockchain.create_transaction(str(message_sender_n)+"_"+str(message_sender_e),message_amount, str(message_receiver_n)+"_"+str(message_reveicer_e),message_timestamp)
                if number_of_transactions==2:
                    number_of_transactions=0
                    local_blockchain.mine(User.public_key,local_blockchain.pending_transactions())

    # TODO Mining
