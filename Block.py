from Transaction import Transaction
from time import time
import hashlib

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
        string_to_hash+=str(previous_hash)
        string_to_hash+=str(nonce)
        string_to_hash+=str(timestamp)
        self.block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
