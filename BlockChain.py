import hashlib
from time import time

from Block import Block
from Transaction import Transaction
from Crypto.PublicKey import RSA


# vanno aggiunte le property, corretti gli underscore e scritte le altre funzioni. A cosa serve replace_chain?


class Blockchain:
    # numero di zeri per il Proof of Work
    difficulty = 2
    # dati per il genesis block, come in Bitcoin
    initial_hash = "The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

    def __init__(self):
        # transazioni non ancora minate
        self.__current_transactions = []
        # Blockchain
        self.__chain = []

    # funzione che crea il primo blocco nella blockchain
    def create_genesis(self, public_key: RSA.RsaKey):
        genesis_block_transactions = self.__current_transactions
        # print("DEBUG_LOG: chiamata a mine() dentro a create_genesis()")
        self.mine(public_key, genesis_block_transactions)
        # print("DEBUG_LOG: mine() dentro a create_genesis() terminata")

    # aggiunge un blocco in coda alla blockchain, se valido
    def add_block(self, block):
        if self.validate_block(block, self.last_block()):
            self.__chain.append(block)
            self.__current_transactions = []
            return True
        return False


    # # # # # # # # # # funzioni di utilità # # # # # # # # # #

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

    def remove_tail(self, index):
        self.__chain = self.__chain[0:index]

    # crea una transazione e la inserisce in __current_transactions
    def create_transaction(self, sender, amount, receiver, sign, timestamp=time()):
        transaction = Transaction(sender, amount, receiver, sign, timestamp)

        if transaction.validate():
            self.__current_transactions.append(transaction)
            return transaction, True
        return None, False

    # funzione per la creazione di un blocco
    def mine(self, reward_address: RSA.RsaKey, new_block_transactions):
        last_block = self.last_block()
        if not last_block:
            previous_hash = self.initial_hash
            index = 0
        else:
            index = last_block.index + 1
            previous_hash = last_block.block_hash

        # transazione di reward per il miner pari a 50 DSSCoin, non ha un mittente
        self.create_transaction(sender="0", amount=50, receiver=str(reward_address.n) + "_" + str(reward_address.e), sign=b"reward")

        # definizione di mining
        # print("DEBUG_LOG: chiamata a generate_proof_of_work() dentro a mine()")
        nonce = self.generate_proof_of_work(new_block_transactions)
        # print("DEBUG_LOG: generate_proof_of_work() dentro a mine() terminata

        block = Block(index, self.__current_transactions, nonce, previous_hash)

        if self.add_block(block):
            return block

        return None

    # cerca un valore (nonce) che concatenato con le informazioni nel blocco
    # produce un hash con difficulty zero in testa
    def generate_proof_of_work(self, block_transactions):

        number = 0 # variabile per l'output
        nonce = 0

        print("Tentativi: ")
        while True:
            # concatenazione dei parametri su cui calcolare l'hash
            if not local_blockchain.last_block():
                string_to_hash = ""
                for i in range(0, len(self.__current_transactions)):
                    string_to_hash += block_transactions[i].sender + str(block_transactions[i].amount) + \
                                      block_transactions[i].receiver + str(block_transactions[i].timestamp)
                string_to_hash += self.initial_hash + str(nonce)
            else:
                string_to_hash = ""
                for i in range(0, len(self.__current_transactions)):
                    string_to_hash += block_transactions[i].sender + str(block_transactions[i].amount) + \
                                      block_transactions[i].receiver + str(block_transactions[i].timestamp)
                string_to_hash += local_blockchain.last_block().block_hash + str(nonce)

            # doppio hash come nel protocollo Bitcoin
            first_hash_256 = hashlib.sha256(string_to_hash.encode()).hexdigest()
            second_hash_256 = hashlib.sha256(first_hash_256.encode()).hexdigest()

            print(str(number) + ": " + second_hash_256)

            # definizione di Proof of Work
            if second_hash_256[:Blockchain.difficulty] == "0" * Blockchain.difficulty:
                print("\n")
                return nonce

            number += 1
            nonce += 1

    # controlla se il blocco ricevuto è coerente con le informazioni possedute
    def validate_block(self, current_block, previous_block: list):
        if not previous_block and current_block.index == 0:
            return True

        elif current_block.index != previous_block.index + 1:
            print(current_block.index)
            print(previous_block.index)
            return False

        if current_block.previous_hash != previous_block.block_hash:
            return False

        string_to_hash = ""
        for i in current_block.transactions:
            string_to_hash += str(i.sender) + str(i.amount) + str(i.receiver)
        string_to_hash += str(self.last_block().block_hash)
        string_to_hash += str(current_block.nonce)
        string_to_hash += str(current_block.timestamp)
        result_hash = hashlib.sha256(string_to_hash.encode()).hexdigest()

        if current_block.block_hash != result_hash:
            return False

        return True

    # verifica la disponibilità nel wallet
    def count_money(self, public_key: RSA.RsaKey):
        amount = 0
        for i in self.__chain:
            for j in i.transactions:
                if j.receiver == str(public_key.n) + "_" + str(public_key.e):
                    amount += int(j.amount)
                if j.sender == str(public_key.n) + "_" + str(public_key.e):
                    amount -= int(j.amount)
        # print("DEBUG_COUNT MONEY"+str(amount))
        for i in self.__current_transactions:
            if i.receiver == str(public_key.n) + "_" + str(public_key.e):
                amount += int(i.amount)
            if i.sender == str(public_key.n) + "_" + str(public_key.e):
                amount -= int(i.amount)
        # print("DEBUG_COUNT MONEY"+str(amount))
        return amount

################################## DA VEDERE SE SERVE #####################################
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

################################## DA VEDERE SE SERVE #####################################
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


# # # # # # # # # # # # # Creazione della Blockchain # # # # # # # # # # # # #

local_blockchain = Blockchain()
