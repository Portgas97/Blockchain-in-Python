from threading import Thread
import socket
import struct
from Crypto.PublicKey import RSA
import User
class ThreadListener(Thread):

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 2000))
        mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            recv=sock.recv(10240)
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
