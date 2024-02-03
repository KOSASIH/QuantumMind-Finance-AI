# Import necessary libraries
from hashlib import sha256
from datetime import datetime

# Define a class for a transaction
class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = datetime.now()

    def calculate_hash(self):
        return sha256((self.sender + self.receiver + str(self.amount) + str(self.timestamp)).encode()).hexdigest()

# Define a class for a block
class Block:
    def __init__(self, previous_hash, transactions):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = datetime.now()
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return sha256((self.previous_hash + str(self.transactions) + str(self.timestamp) + str(self.nonce)).encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

# Define a class for the blockchain
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 10

    def create_genesis_block(self):
        return Block("0", [])

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_address):
        block = Block(self.get_latest_block().hash, self.pending_transactions)
        block.mine_block(self.difficulty)
        self.chain.append(block)

        self.pending_transactions = [
            Transaction("network", miner_address, self.mining_reward)
        ]

    def create_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        self.pending_transactions.append(transaction)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.sender == address:
                    balance -= transaction.amount
                elif transaction.receiver == address:
                    balance += transaction.amount
        return balance

# Create an instance of the blockchain
blockchain = Blockchain()

# Create transactions
blockchain.create_transaction("address1", "address2", 10)
blockchain.create_transaction("address2", "address1", 5)

# Mine pending transactions
blockchain.mine_pending_transactions("miner_address")

# Get balance of addresses
balance1 = blockchain.get_balance("address1")
balance2 = blockchain.get_balance("address2")
balance_miner = blockchain.get_balance("miner_address")

# Print balances
print("Balance of address1:", balance1)
print("Balance of address2:", balance2)
print("Balance of miner_address:", balance_miner)
