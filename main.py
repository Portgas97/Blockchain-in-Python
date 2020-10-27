from Block import Block
import User


def add_block(transaction):
    if not BlockChain:
        new_block = Block("Chanceller on the brink...", transaction)
        BlockChain.insert(0, new_block)
    else:
        new_block = Block(BlockChain[0].block_hash, transaction)
        BlockChain.insert(0, new_block)


BlockChain = []


add_block(["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"])

add_block(["Satoshi sent 1 BTC to Ivan", "Maria sent 5 MTC to Jenny", "Satoshi sent 5 BTC to Hal Finney"])

for i in range(len(BlockChain)):
    print(BlockChain[i].block_hash)

public, private = User.newkeys(1024)

c = User.crypt("ciao".encode(), public)
print(c)
d = User.decrypt(c, private)
print(d.decode())

ciao=private.exportKey()
print(ciao.decode())

