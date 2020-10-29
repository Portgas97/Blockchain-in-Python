from threading import Thread
import socket
import struct
from Crypto.PublicKey import RSA
import User

class ThreadListener(Thread):

    # metodo che rappresenta le attività compiute dal thread
    def run(self):
        # creazione del socket, utilizza IPv4, di tipo UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # SO_REUSEADDR è u flag che dice al kernel di riusare un socket locale nello stato 'TIME_WAIT', senza aspettare per il timeout
        # level = SOL_SOCKET implica che manipoliamo a livello di API
        # SO_REUSEADDR dice al kernel di riusare indirizzi locali se sono nello stato di TIME_WAIT anche prima della scadenza del timeout
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
            recv=sock.recv(10240) # non recvfrom per multicasting
            message_arrived=recv.split(b'&&')
            sign=message_arrived[1];
            encrypted_message=message_arrived[0].split(b'&')
            received_sender_public_key=encrypted_message[0]
            amount=encrypted_message[1]
            received_receiver_public_key=encrypted_message[2]

            sender_public_key=RSA.import_key(received_sender_public_key)
            receiver_public_key=RSA.import_key(received_receiver_public_key)
            is_valid=User.verify(message_arrived[0],sign,sender_public_key)
            print("Transiction is valid:"+str(is_valid))

    # TODO Mining
