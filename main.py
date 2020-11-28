import User
from Listener import ThreadListener
from ServerListener import BlockListener
from BlockChain import local_blockchain, Blockchain
import os
import signal
from Crypto.PublicKey import RSA

print("---------------------------------------------------")
print("|                                                 |")
print("| Welcome to DSSCoin, type \'register\' or \'login\': |")
print("|                                                 |")
print("---------------------------------------------------")

# get the user operation
op = input()

if op == "register":
    print("Registration: operation started...")
    # print("DEBUG_LOG: call User.register()")
    public, private = User.register()

else:
    if op == "login":
        print("Insert your private key:")
        key = input()
        User.update_blockchain()
        print("Login operation started...")
        # print("DEBUG_LOG: call User.login()")
        public, private = User.login(key)
        if public is None and private is None:
            print("Login: The key inserted doesn't exist")
            print("Registration: operation started...")
            public, private = User.register()
    else:
        public = private = None
        print("Wrong operation! I'm exiting with error")
        os.kill(os.getpid(), signal.SIGTERM)

# User.send_money(private, public)
print("Checking Blockchain: operation started\n")

if not User.exists_blockchain():
    print("Creating Genesis Block\n")
    # print("DEBUG_LOG: call create_genesis()\n")
    Blockchain.create_genesis(local_blockchain, public)
    # print("DEBUG_LOG: create_genesis() ended")
else:
    print("Synchronizing Blockchain")
    # print("DEBUG_LOG: call update_blockchain()")
    User.update_blockchain()
    # print("DEBUG_LOG: update_blockchain() ended")

print("Checking Blockchain: operation terminated\n")
# print("DEBUG_LOG: start listener thread")

# This thread listen to exists and update requests. This thread also listen to transaction incoming from the network.
listener = ThreadListener()
listener.start()

# This thread listen to blocks mined from other peers.
block_listener = BlockListener()
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

    # get the operation desired
    op = int(input())

    if op > 4 or op < 1:  # error
        print("I'm exiting with error")
        os.kill(os.getpid(), signal.SIGTERM)

    elif op == 1:  # send money
        # print("DEBUG_LOG: call send_money()")
        print("Send money started")
        User.send_money(private, public)
        # print("DEBUG_LOG: send_money() ended")

    elif op == 2:  # show the blockchain
        print("Actual Blockchain:")
        local_blockchain.print()

    elif op == 3:  # history of transaction of the user
        print("Transaction History:")
        print("Insert public key:")
        key_input = input()
        public_key = key_input.split("_")
        if key_input != "":
            local_blockchain.print_user_transactions(RSA.construct((int(public_key[0]), int(public_key[1]))))
        else:
            local_blockchain.print_user_transactions(public)

    elif op == 4:  # exit
        print("########### THE END ###########")
        os.kill(os.getpid(), signal.SIGTERM)
