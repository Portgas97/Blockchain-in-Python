import hashlib
from Block import Block
from Transaction import Transaction


# vanno aggiunte le property, corretti gli underscore e scritte le altre funzioni. A cosa serve replace_chain?

class Blockchain:
    difficulty = 4

    def __init__(self):
        #
        self.__current_transactions = []
        self.__chain = []
        self.create_genesis()

    def create_genesis(self):
        genesis_block = Block(0, self.__current_transactions, 0, '00')
        self.__chain.append(genesis_block)

    def add_block(self, block):
        if self.validate_block(block, self.last_block):
            self.__chain.append(block)
            self.__current_transactions = []
            return True
        return False

    def last_block(self):
        if not self.__chain:
            return []
        return self.__chain[-1]

    def last_transaction(self):
        return self.__current_transactions[-1]

    def pending_transactions(self):
        return self.__current_transactions

    def full_chain(self):
        return self.__chain


def create_transaction(self, sender, receiver, amount):
    transaction = Transaction(sender, receiver, amount)

    if transaction.validate():  # todo aggiungere controllo soldi disponibili a validate()
        self.__current_transactions.append(transaction)
        return transaction, True
    return None, False


def mine(self, reward_address):
    last_block = self.last_block
    index = last_block.index + 1
    previous_hash = last_block.hash

    nonce = self.generate_proof_of_work(last_block)

    # transaction to reward the miner, no sender
    self.create_transaction(sender="0", receiver=reward_address, amount=1)

    block = Block(index, self.__current_transactions, nonce, previous_hash)

    if self.add_block(block):
        return block

    return None


@staticmethod
def validate_proof_of_work(last_nonce, last_hash, nonce):
    pass


def generate_proof_of_work(self, block):
    while True:
        nonce = 0
        string_to_hash = "".join(block.transactions) + last_block(self).block_hash + nonce
        first_hash_256 = hashlib.sha256(string_to_hash.encode()).hexdigest()
        second_hash_256 = hashlib.sha256(first_hash_256.encode()).hexdigest()
        if second_hash_256[:Blockchain.difficulty] == "0" * Blockchain.difficulty:
            return second_hash_256, nonce
        nonce += 1


def validate_block(self, current_block, previous_block):
    if current_block.index != previous_block.index + 1:
        return False

    if current_block.previous_hash != previous_block.block_hash:
        return False

    string_to_hash = "".join(self.transaction) + self.previous_hash
    result_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()
    if current_block.hash != result_hash:
        return False

    # da aggiungere if non valido PoW
    return True


def validate_chain(self, chain_to_validate):
    pass


def replace_chain(self, new_chain):
    pass





# AGGIUNGI TEST

local_blockchain = Blockchain()