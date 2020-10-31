import hashlib
from Block import Block
from Transaction import Transaction


# vanno aggiunte le property, corretti gli underscore e scritte le altre funzioni. A cosa serve replace_chain?

class Blockchain:

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


def create_transaction(self, sender, receiver, amount):
    transaction = Transaction(sender, receiver, amount)

    if transaction.validate():
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
    pass


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


@property
def last_block(self):
    return self.__chain[-1]


@property
def last_transaction(self):
    return self.__current_transactions[-1]


@property
def pending_transactions(self):
    return self.__current_transactions


@property
def full_chain(self):
    return self.__chain


# AGGIUNGI TEST

Blockchain = BlockChain()
BlockChain.create_genesis()
