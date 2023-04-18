import json
from src import block
import time
from datetime import datetime


class Node:
    """A class representing a node in a blockchain."""
    def __init__(self, server_id):
        self.server_id = server_id
        self.blocks = []  # a list to store all the blocks
        self.last_block = None

    def create_new_block(self):
        """Creates new block"""
        index = self.last_block.index + 1 # index of new block
        prev_hash = self.last_block.hash  # prev_hash of new block
        nonce_type = self.server_id  # nonce of new block
        timestamp = datetime.now().time()
        return block.Block(index, prev_hash, nonce_type, timestamp)

    def handle_received_block(self, received_block):
        """Handle received blocks"""
        block_json = json.loads(received_block)
        rec_block = block.from_json(block_json)

        if rec_block.index == 0:
            # If genesis, appends to chain
            self.blocks.append(rec_block)
            self.last_block = rec_block
            rec_block.print_block(0, True)
            return True

        last_index = 0
        if self.last_block is not None:
            last_index = self.last_block.index

        if rec_block.index == last_index + 1:
            # If block is valid, appends to chain
            self.blocks.append(rec_block)
            self.last_block = rec_block
            rec_block.print_block(int(block_json['server_id']), False)
            return True

        if rec_block.index == last_index and rec_block.timestamp < self.last_block.timestamp:
            self.blocks[-1] = rec_block
            self.last_block = rec_block
            rec_block.print_block(int(block_json['server_id']), False)
            time.sleep(1)
            return True

        return False

    def add_genesis(self):
        """Create and add GENESIS block"""
        genesis = block.create_genesis()
        self.blocks.append(genesis)
        self.last_block = genesis
        genesis.print_block(1, True)
        return genesis

    def is_valid(self):
        """Check if the chain is valid"""
        for i in range(1, len(self.blocks)):
            current_block = self.blocks[i]
            prev_block = self.blocks[i - 1]

            if prev_block.hash != current_block.prev_hash:
                return False
        return True

    def to_string(self, length):
        """Converts blocks to string"""
        str_chain = ""
        for i in range(length):
            chain_block = self.blocks[i]
            str_chain += chain_block.__str__() + "\n"

        return str_chain
