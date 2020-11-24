import User
from Listener import ThreadListener
from ServerListener import BlockListener
from BlockChain import local_blockchain, Blockchain
import os
import signal
import sys
import time


# add_block(["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"])
# add_block(["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"])
# for i in range(len(BlockChain)):
#    print(BlockChain[i].block_hash)
# public, private = User.newkeys(1024)




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
    #time.sleep(2)
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
print("Checking Blockchain: operation started\n")



if not User.exists_blockchain():
    print("Creating Genesis Block\n")
    print("DEBUG_LOG: chiamata a create_genesis()\n")
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




# Queste operazioni vanno all'interno di un ciclo infinito in modo da poter rieseguire
while True:
    # DEBUG - each process prints the hash of the last block (in this case, the genesis block)
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



#time.sleep(10)
print("sleep in User.py terminata")

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
