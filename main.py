import socket
import User
from Listener import ThreadListener
from BlockChain import local_blockchain, Blockchain

#add_block(["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"])
#add_block(["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"])
#for i in range(len(BlockChain)):
#    print(BlockChain[i].block_hash)
#public, private = User.newkeys(1024)

listener = ThreadListener()
listener.start()


print("Welcome to DSSCoin, type \'register\' or \'login\':")
op=input()
if op == "register":
    public, private = User.register()
else:
    if op == "login":
        print("Insert your private key:")
        key = input();
        public, private = User.login(key)
    else:
        print("Wrong operation! I'm exiting with error")
        exit(-1)

#User.send_money(private, public)

if not User.exists_blockchain():
    Blockchain.create_genesis(local_blockchain)
else:
    User.update_blockchain()

#c = User.crypt("ciao".encode(), public)
#print(c)
#d = User.decrypt(c, private)
#print(d.decode())

#ciao = public.exportKey()
#print(ciao.decode())

#listener = ThreadListener()
#listener.start()

#prova=["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"]

#time.sleep(1)
#sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
#sock.sendto("".join(prova).encode(), ("224.0.0.0", 2000))

#n=private.n
#e=private.e
#d=private.d
#p=private.p
#q=private.q

#print(n)
#print(e)
#print(d)

#nuova=RSA.construct([n,e,d,p,q],consistency_check=True)
#print(nuova.exportKey().decode())
