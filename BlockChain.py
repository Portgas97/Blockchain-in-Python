import hashlib
from Block import Block
from Transaction import Transaction
from Crypto.PublicKey import RSA
# vanno aggiunte le property, corretti gli underscore e scritte le altre funzioni. A cosa serve replace_chain?
global public

class Blockchain:
    difficulty = 4

    def __init__(self):
        #
        self.__current_transactions = []
        self.__chain = []

    def create_genesis(self, public_key: RSA.RsaKey):
        genesis_block = Block(0, self.__current_transactions, 0, '00')
        #self.mine(public_key, genesis_block)
        self.__chain.append(genesis_block)

    def add_block(self, block):
        if self.validate_block(block, self.last_block()):
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

    def get_chain(self):
        return self.__chain

    def get_last_hash(self):
        return self.__chain[-1].block_hash

    def create_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)

        if transaction.validate():  # todo aggiungere controllo soldi disponibili a validate()
            self.__current_transactions.append(transaction)
            return transaction, True
        return None, False

    def mine(self, reward_address:RSA.RsaKey,new_block: Block):
        last_block = self.last_block()
        if not last_block:
            previous_hash="Hash di partenza"
            index=0
        else:
            index = last_block[0].index + 1
            previous_hash = last_block.hash

        # definizione di Mining
        nonce = self.generate_proof_of_work(new_block)

        # transaction to reward the miner, no sender
        self.create_transaction(sender="0", receiver=str(reward_address.n)+"_"+str(reward_address.e), amount=1)

        block = Block(index, self.__current_transactions, nonce, previous_hash)

        if self.add_block(block):
            return block

        return None

    def validate_proof_of_work(self, last_nonce, last_hash, nonce):
        # f è per la formattazione
        sha = hashlib.sha256(f'{last_nonce}{last_hash}{nonce}'.encode())
        return sha.hexdigest()[:4] == '0' * Blockchain.difficulty

    def generate_proof_of_work(self, block):
        nonce=0
        while True:
            # concatenazione dei parametri su cui calcolare l'hash
            if not local_blockchain.last_block():
                string_to_hash = "".join(block.transactions) + "hash di partenza" + str(nonce)
            else:
                string_to_hash = "".join(block.transactions) + local_blockchain.last_block().block_hash + nonce

            # doppio hash come nel protocollo Bitcoin
            first_hash_256 = hashlib.sha256(string_to_hash.encode()).hexdigest()
            second_hash_256 = hashlib.sha256(first_hash_256.encode()).hexdigest()
            # definizione di Proof of Work
            print(second_hash_256)
            if second_hash_256[:Blockchain.difficulty] == "0" * Blockchain.difficulty:
                #ho rimosso il return double hash, non dovrebbe essere un problema
                return nonce
            nonce += 1

    def validate_block(self, current_block, previous_block: list):
        if not previous_block and current_block.index == 0:
            return True

        elif current_block.index != previous_block.index + 1:
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

        # Validate genesis blocks
        sha1 = hashlib.sha256("".join(self.__chain[0].transactions).encode()).hexdigest()
        sha2 = hashlib.sha256("".join(chain_to_validate[0].transactions).encode()).hexdigest()
        if sha1 != sha2:
            return False

        # Then we compare each block with its previous one
        for x in range(1, len(chain_to_validate)):
            if not self.validate_block(chain_to_validate[x], chain_to_validate[x - 1]):
                return False

        return True

    def replace_chain(self, new_chain):

        # We replace only if the new chain is bigger than the current one
        if len(new_chain) <= len(self.__chain):
            return False

        # Validate the new chain
        if not self.validate_chain(new_chain):
            return False

        # Add blocks
        new_blocks = new_chain[len(self.__chain):]
        for block in new_blocks:
            self.add_block(block)


# AGGIUNGI TEST

local_blockchain = Blockchain()
