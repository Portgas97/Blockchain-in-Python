import hashlib
from time import time
from Transaction import Transaction
class Block:
    def __init__(self, index, transactions:list, nonce, previous_hash, timestamp=time()):
        self.index = index
        self.transactions = transactions
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        string_to_hash = ""#.join(transactions) + previous_hash
        for i in transactions:
            string_to_hash+=str(i.sender)+str(i.amount)+str(i.receiver)
        string_to_hash+=previous_hash
        self.block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
