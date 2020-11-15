from BlockChain import local_blockchain
from Crypto.PublicKey import RSA
from threading import Thread
import BlockChain
import hashlib
import base64
import socket
import struct
import Block
import time
import User
import json

TRANSACTIONS_IN_BLOCK = 2

class ThreadListener(Thread):

    # define the activities of a thread such as respond to requests or transactions
    def run(self):

        # creazione del socket, utilizza IPv4, di tipo UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # SO_REUSEADDR è u flag che dice al kernel di riusare un socket locale nello stato 'TIME_WAIT', senza aspettare per il timeout
        # level = SOL_SOCKET implica che manipoliamo a livello di API
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock1.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

        # '' equivale a INADDR_ANY, si fa il bind su tutte le interfacce
        sock.bind(('', 2000))

        # funzione che converte i valori passati in un bytes object secondo le modalità espresse da format
        # s = char (4s significa 4 byte), l = long, = native byte order + standard size and alignment
        # 224.0.0.0 è uno degli indirizzi adibiti al multicast
        mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)

        # aggiungiamo al multicast group
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # count transactions
        number_of_transactions = 0


        def exists():
            if not local_blockchain.get_chain():
                sock1.sendto("False".encode(), ("224.0.0.0", 2001))
            if local_blockchain.get_chain():
                sock1.sendto("True".encode(), ("224.0.0.0", 2001))


        def send_json(ini, index):
            packets = []

            for i in range(0, index + 1):
                new_block = local_blockchain.get_chain()[i]
                # print("DEGUG_LOG"+ str(new_block.index))
                transactions = new_block.transactions
                # print(transactions)
                dict_tra = []

                for j in range(0, len(transactions)):
                    new_dict = {
                        "sender": transactions[j].sender,
                        "amount": transactions[j].amount,
                        "receiver": transactions[j].receiver,
                        "timestamp": transactions[j].timestamp,
                        "sign": f"{transactions[j].sign}"
                    }
                    dict_tra.append(new_dict)
                    # fine for su j
                # print(dict_tra)
                dict_transactions = {k: dict_tra[k] for k in range(0, len(transactions))}

                new_packet = {
                    "index": new_block.index,
                    "transactions": dict_transactions,
                    "nonce": new_block.nonce,
                    "previous_hash": new_block.previous_hash,
                    "timestamp": new_block.timestamp
                }
                packets.append(new_packet)
                # fine for su i

            if ini == 0:
                dict = {i: packets[i] for i in range(0, index + 1)}
            else:
                dict = {i: packets[i] for i in range(ini + 1, index + 1)}

            json_packet = json.dumps(dict)
            sock1.sendto(json_packet.encode(), ("224.0.0.0", 2001))


        def update():
            tmp = recv.decode().split(" ")

            last_block = tmp[1]
            received_public_key = tmp[2]

            if received_public_key == str(User.public_key.n) + "_" + str(User.public_key.e):
                print("non rispondo a me stesso")
                return

            # CASO IN CUI IL MITTENTE NON HA NIENTE
            if last_block == "empty":
                index = BlockChain.local_blockchain.last_block().index
                send_json(0, index)

            # CASO IN CUI NON C'È BISOGNO DI AGGIORNARE
            elif int(last_block) == BlockChain.local_blockchain.last_block().index:
                # print("DEBUG last block:" + last_block)
                # print("DEBUG localblockchain.lastblock"+str(BlockChain.local_blockchain.last_block().index))
                sock1.sendto("Already up to date".encode(), ("224.0.0.0", 2001))

            # CASO IN CUI C'È UN AGGIORNAMENTO PARZIALE
            elif int(last_block) < BlockChain.local_blockchain.last_block().index:
                index = BlockChain.local_blockchain.last_block().index
                send_json(int(last_block), index)

            # CASO DI INDICE NON VALIDO
            elif int(last_block) > BlockChain.local_blockchain.last_block().index:
                # print("Index not valid")
                sock1.sendto("index_error".encode(), ("224.0.0.0", 2001))


        def handle_transaction(number_of_transactions):
            message_arrived = recv.split(b'divisore')

            sign = message_arrived[1]
            message = json.loads(message_arrived[0].decode())

            # ricavo i sottocampi
            message_sender_n = message["sender_n"]
            message_sender_e = message["sender_e"]
            message_amount = message["amount"]
            message_receiver_n = message["receiver_n"]
            message_reveicer_e = message["receiver_e"]
            message_timestamp = message["timestamp"]
            message_sign = eval(message["sign"])

            print(message_sign)
            print(type(message_sign))

            message.pop("sign") # Toglie dal dizionario la firma e poi controlla che sia tutto ok

            key_received = str(message_sender_n) + "_" + str(message_sender_e)
            local_private_key = str(User.public_key.n) + "_" + str(User.public_key.e)

            if key_received == local_private_key:
                # torno in ascolto
                local_blockchain.create_transaction(key_received, message_amount,
                                                    str(message_receiver_n) + "_" + str(message_reveicer_e),
                                                    message_timestamp)
                # print("DEBUG_LOG: il thread listener ha ricevuto una transazione creata in locale")
                return number_of_transactions

            sender_key = RSA.construct([message_sender_n, message_sender_e])
            is_valid = User.verify(message.__str__().encode(), message_sign, sender_key)
            print("Transaction is valid:" + str(is_valid))

            number_of_transactions = number_of_transactions + 1
            local_blockchain.create_transaction(str(message_sender_n) + "_" + str(message_sender_e), message_amount,
                                                str(message_receiver_n) + "_" + str(message_reveicer_e), message_sign,
                                                message_timestamp)  # message sign already evaluated

            # Se ho raccolto un numero sufficiente di transazioni comincio a minare il blocco
            if number_of_transactions == TRANSACTIONS_IN_BLOCK:
                number_of_transactions = 0

                block_mined = local_blockchain.mine(User.public_key, local_blockchain.pending_transactions())
                print("Block mined successfully")
                print(block_mined)

                new_packet = ""

                if block_mined is not None:
                    print("Debug-I'm sending the block just mined!")
                    transactions = block_mined.transactions
                    # print(transactions)
                    dict_tra = []

                    for j in range(0, len(transactions)):
                        new_dict = {
                            "sender": transactions[j].sender,
                            "amount": transactions[j].amount,
                            "receiver": transactions[j].receiver,
                            "timestamp": transactions[j].timestamp,
                            "sign": f"{transactions[j].sign}"
                        }
                        dict_tra.append(new_dict)

                    dict_transactions = {k: dict_tra[k] for k in range(0, len(transactions))}

                    new_packet = {
                        "index": block_mined.index,
                        "transactions": dict_transactions,
                        "nonce": block_mined.nonce,
                        "previous_hash": block_mined.previous_hash,
                        "timestamp": block_mined.timestamp,

                    }

                json_block = json.dumps(new_packet)
                sock1.sendto(json_block.encode(), ("224.0.0.0", 2002))

            return number_of_transactions


        while True:
            print("DEBUG_LOG: Listener torna ad eseguire while true, ascolto...")
            recv = sock.recv(10240)  # non si usa recvfrom per multicasting

            msg = " "
            try:
                msg = recv.decode()
            except:
                print(msg)

            if msg == "exists": # Richiesta di esistenza della blockchain
                exists()

            elif msg[:6] == "update": # Richiesta di aggiornamento della blockchain
                update()

            else: # Ricezione di una transazione
                number_of_transactions = handle_transaction(number_of_transactions)
