
import User
from Listener import ThreadListener
from BlockChain import local_blockchain, Blockchain
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
    public, private = User.register()
else:
    if op == "login":
        print("Insert your private key:")
        key = input()
        print("Login in corso...")
        public, private = User.login(key)
    else:
        print("Wrong operation! I'm exiting with error")
        exit(-1)


# User.send_money(private, public)
# DEBUG
print("Checking Blockchain: operation started")


if not User.exists_blockchain():
    print("Creating Genesis Block")
    Blockchain.create_genesis(local_blockchain)
else:
    print("Synchronizing Blockchain")
    User.update_blockchain()

listener = ThreadListener()
listener.start()
# DEBUG
print("Checking Blockchain: operation terminated")
# TODO: che operazioni vuole fare l'utente ?
# Inviare denaro
# Visualizzare la Blockchain
# Conoscere la storia delle sue transazioni / wallet, forse questo implica una classe Utente e la gestione con i file

print(local_blockchain.get_last_hash())
time.sleep(20)
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
