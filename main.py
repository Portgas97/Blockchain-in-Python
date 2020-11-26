import User
from Listener import ThreadListener
from ServerListener import BlockListener
from BlockChain import local_blockchain, Blockchain
import os
import signal



print("---------------------------------------------------")
print("|                                                 |")
print("| Welcome to DSSCoin, type \'register\' or \'login\': |")
print("|                                                 |")
print("---------------------------------------------------")

# leggo l'operazione dell'utente
op = input()

if op == "register":
    print("Registrazione in corso...")
    # print("DEBUG_LOG: chiamata a User.register()")
    public, private = User.register()

else:
    if op == "login":
        print("Insert your private key:")
        key = input()
        print("Login operation started...")
        # print("DEBUG_LOG: chiamata a User.login()")
        public, private = User.login(key)
    else:
        print("Wrong operation! I'm exiting with error")
        os.kill(os.getpid(), signal.SIGTERM)

# User.send_money(private, public)
print("Checking Blockchain: operation started\n")



if not User.exists_blockchain():
    print("Creating Genesis Block\n")
    # print("DEBUG_LOG: chiamata a create_genesis()\n")
    Blockchain.create_genesis(local_blockchain, public)
    # print("DEBUG_LOG: create_genesis() terminata")
else:
    print("Synchronizing Blockchain")
    # print("DEBUG_LOG: chiamata a update_blockchain()")
    User.update_blockchain()
    # print("DEBUG_LOG: update_blockchain() terminata")

print("Checking Blockchain: operation terminated\n")
# print("DEBUG_LOG: avvio del thread listener")
listener = ThreadListener()
listener.start()

block_listener=BlockListener()
block_listener.start()





while True:
    # DEBUG - each process prints the hash of the last block (in this case, the genesis block)
    print("\n")
    print("Hash of the current block: ")
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

    # leggo l'operazione desiderata
    op = int(input())

    if op > 4 or op < 1: # errore
        print("I'm exiting with error")
        os.kill(os.getpid(), signal.SIGTERM)

    elif op == 1: # send money
        # print("DEBUG_LOG: chiamata a send_money()")
        print("Send money started")
        User.send_money(private, public)
        # print("DEBUG_LOG: send_money() terminata")

    elif op == 2: # show the blockchain
        print("Actual Blockchain:")
        local_blockchain.print()

    elif op == 3: # history of transaction of the user
    # Potremmo leggere anche la chiave pubblica e vedere il portafogli di un qualunque utente ???
        print("Transaction History:")
        local_blockchain.print_user_transactions(public)

    elif op == 4: # exit
        print("########### FINE DEMO ###########")
        os.kill(os.getpid(), signal.SIGTERM)
