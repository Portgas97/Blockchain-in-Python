import hashlib
from time import time


class Block:
    def __init__(self, index, transactions, nonce, previous_hash):

        self.index = index
        self.transactions = transactions
        self.nonce = nonce
        self.previous_hash = previous_hash
        self.timestamp = time()
        string_to_hash = "".join(transactions) + previous_hash
        self.block_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
