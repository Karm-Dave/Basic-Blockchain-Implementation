import hashlib
import json
from time import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        main_dict=self.__dict__.copy()
        main_dict.pop('hash',None)
        block_string = json.dumps(main_dict, sort_keys=True)
        # print(f"Block String for Hash Calculation: {block_string}")  # Debug print
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block(0, "0", time(), "Genesis Block")

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, data):
        last_block = self.get_last_block()
        new_block = Block(len(self.chain), last_block.hash, time(), data)
        new_block = self.mine_block(new_block)
        self.chain.append(new_block)

    def mine_block(self, block):
        block.nonce = 0
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
            # print(f"Mining: nonce={block.nonce}, hash={block.hash}")  # Debug print
        return block

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Recalculate hash for the current block
            recalculated_hash = current_block.calculate_hash()

            # Debug prints
            # print(f"Block Data: {current_block.nonce}")

            # print(f"Current Block Hash: {current_block.hash}")
            # print(f"Recalculated Hash: {recalculated_hash}")
            
            if current_block.hash != recalculated_hash:
                # print(f"Invalid hash at index {i}")
                return False

            if current_block.previous_hash != previous_block.hash:
                # print(f"Invalid previous hash at index {i}")
                return False
        return True
