from BlockChain import local_blockchain, Blockchain
from ServerListener import BlockListener
from Listener import ThreadListener
import signal
import User
import time
import sys
import os


print("---------------------------------------------------")
print("|                                                 |")
print("| Welcome to DSSCoin, type \'register\' or \'login\': |")
print("|                                                 |")
print("---------------------------------------------------")

op = input()

if op == "register":
    print("Registrazione in corso...")
    print("DEBUG_LOG: chiamata a User.register()")
    public, private = User.register()

else:
    if op == "login":
        print("Insert your private key:")

        key = input()

        print("Login in corso...")
        print("DEBUG_LOG: chiamata a User.login()")

        public, private = User.login(key)

    else:
        print("Wrong operation! I'm exiting with error")
        os.kill(os.getpid(), signal.SIGTERM)

# User.send_money(private, public)
print("Checking Blockchain: operation started")



if not User.exists_blockchain():
    print("Creating Genesis Block\n")

    print("DEBUG_LOG: chiamata a create_genesis()")
    Blockchain.create_genesis(local_blockchain, public)
    print("DEBUG_LOG: create_genesis() terminata")

else:
    print("Synchronizing Blockchain")

    print("DEBUG_LOG: chiamata a update_blockchain()")
    User.update_blockchain()
    print("DEBUG_LOG: update_blockchain() terminata")

print("Checking Blockchain: operation terminated\n")
print("DEBUG_LOG: avvio del thread listener")

listener = ThreadListener()
listener.start()

block_listener=BlockListener()
block_listener.start()


while True:
    # DEBUG - each process prints the hash of the last block

    print("\n")
    print("Hash del blocco corrente")
    print(local_blockchain.get_last_hash())
    print("\n")
    print("---------------------------------------------------")
    print("|                                                 |")
    print("| Available functions:                            |")
    print("| (insert a number between 1 and 4)               |")
    print("|    1) Send money                                |")
    print("|    2) Show the Blockchain                       |")
    print("|    3) History of transactions                   |")
    print("|    4) Exit                                      |")
    print("|                                                 |")
    print("---------------------------------------------------")
    # transform in float ???
    op = int(input())

    if op > 4 or op < 1:
        print("I'm exiting")
        os.kill(os.getpid(), signal.SIGTERM)

    elif op == 1:
        print("DEBUG_LOG: chiamata a send_money()")
        User.send_money(private, public)
        print("DEBUG_LOG: send_money() terminata")

    elif op == 2:
        print("Actual Blockchain:")

    elif op == 3:
        print("Transaction History:")

    elif op == 4:
        User.update_blockchain()


print("####### FINE DEMO #######")

# c = User.crypt("ciao".encode(), public)
# print(c)
# d = User.decrypt(c, private)
# print(d.decode())

# ciao = public.exportKey()
# print(ciao.decode())

# listener = ThreadListener()
# listener.start()

# prova=["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"]

# time.sleep(1)
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
# sock.sendto("".join(prova).encode(), ("224.0.0.0", 2000))

# n=private.n
# e=private.e
# d=private.d
# p=private.p
# q=private.q

# print(n)
# print(e)
# print(d)

# nuova=RSA.construct([n,e,d,p,q],consistency_check=True)
# print(nuova.exportKey().decode())
