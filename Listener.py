from threading import Thread
import socket
import struct


class ThreadListener(Thread):

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 2000))
        mreq = struct.pack("=4sl", socket.inet_aton("224.0.0.0"), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            print(sock.recv(10240).decode())
    # TODO Mining
