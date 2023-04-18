import json
import random
import string
from hashlib import sha256
from datetime import datetime


def generate_random_data(length):
    """Generate a random string of the given length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))


class Block:
    """A class representing a block in a blockchain."""

    RANDOM_DATA_LENGTH = 256
    MIN_NONCE_INCREMENT = 1
    MAX_NONCE_INCREMENT_TYPE_1 = 10
    MAX_NONCE_INCREMENT_TYPE_2 = 20
    MAX_NONCE_INCREMENT_TYPE_3 = 30

    def __init__(self, index: int, prev_hash: str, nonce_type: int, time):
        """Initialize a new Block object."""
        self.index = index  # block index
        self.prev_hash = prev_hash  # hash of previous block
        self.data = generate_random_data(self.RANDOM_DATA_LENGTH)  # block data
        self.nonce = 0  # initial nonce
        self.hash = self.mine_block(nonce_type)  # mine the block to get its hash
        self.timestamp = time

    def __str__(self):
        """Return a string representation of the block."""
        return f"Block (index={self.index}, prev_hash={self.prev_hash}, hash={self.hash}, data={self.data}, " \
               f"nonce={self.nonce})"

    def mine_block(self, nonce_type):
        """Mine the block to get its hash."""
        while True:
            block_str = f"{self.index}{self.prev_hash}{self.data}{self.nonce}"
            block_hash = sha256(block_str.encode()).hexdigest()
            if block_hash.endswith("0000"):
                return block_hash
            self.nonce += self.get_nonce_increment(nonce_type)

    def get_nonce_increment(self, nonce_type):
        """Get the nonce increment based on the nonce type."""
        if nonce_type == 1:
            return random.randint(self.MIN_NONCE_INCREMENT, self.MAX_NONCE_INCREMENT_TYPE_1)
        elif nonce_type == 2:
            return random.randint(self.MAX_NONCE_INCREMENT_TYPE_1 + 1, self.MAX_NONCE_INCREMENT_TYPE_2)
        else:
            return random.randint(self.MAX_NONCE_INCREMENT_TYPE_2 + 1, self.MAX_NONCE_INCREMENT_TYPE_3)

    def to_dict(self, server_id):
        """Convert the block to a dictionary."""
        return {
            "index": self.index,
            "hash": self.hash,
            "prev_hash": self.prev_hash,
            "data": self.data,
            "nonce": self.nonce,
            "server_id": server_id,
            "timestamp": str(self.timestamp)
        }

    def to_json(self, server_id):
        """Convert the block to a JSON string."""
        return json.dumps(self.to_dict(server_id))

    def print_block(self, server_id, flag):
        """Print block"""
        if flag:
            print(f"Initialized GENESIS:  {self.__str__()}")
        else:
            print(f"Received a block from Node {server_id}:  {self.__str__()}")


def create_genesis():
    """Create the genesis block."""
    genesis_block = Block(index=0, prev_hash="GENESIS", nonce_type=0, time=datetime.now().time())
    return genesis_block


def from_json(json_block):
    """Convert JSON string to a block."""
    conv_block = Block(
        int(json_block['index']),
        json_block['prev_hash'],
        json_block['server_id'],
        datetime.strptime(json_block['timestamp'], '%H:%M:%S.%f').time()
    )
    conv_block.hash = json_block['hash']
    conv_block.nonce = json_block['nonce']
    conv_block.data = json_block['data']
    return conv_block
