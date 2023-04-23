import json
import random

from src import block


def test_block_init():
    for i in range(5):
        block_index = random.randint(1, 100000)
        nonce_type = random.randint(1, 3)
        prev_hash = 'test_init'

        new_block = block.Block(block_index, prev_hash, nonce_type, None)

        assert new_block is not None

        assert new_block.hash is not None
        assert new_block.data is not None
        assert new_block.index is not None
        assert new_block.prev_hash is not None
        assert new_block.nonce is not None


def test_block_init_creates_unique_block_hashes():
    for i in range(5):
        # Create two blocks with the same attributes and ensure their hashes are different
        block_index = random.randint(1, 100000)
        nonce_type = random.randint(1, 3)
        prev_hash = 'test_init'

        new_block1 = block.Block(block_index, prev_hash, nonce_type, None)
        new_block2 = block.Block(block_index, prev_hash, nonce_type, None)

        assert new_block1.hash != new_block2.hash


def test_mine_creates_block_with_hash_ending_in_zeros():
    for i in range(5):
        block_index = 1
        prev_hash = 'mine_test'
        nonce_type = 1
        current_block = block.Block(block_index, prev_hash, nonce_type, None)

        assert type(current_block.hash) == str
        assert current_block.hash[-4:] == "0000"
        assert current_block.prev_hash == 'mine_test'


def test_block_to_json():
    for i in range(5):
        block_index = random.randint(1, 100000)
        prev_hash = 'json_test'
        nonce_type = random.randint(1, 3)
        server_id = random.randint(1, 3)

        new_block = block.Block(block_index, prev_hash, nonce_type, None)

        json_block = new_block.to_json(server_id)
        assert type(json_block) == str

        python_object = json.loads(json_block)

        index = int(python_object['index'])
        cur_hash = python_object['hash']
        prev_hash = python_object['prev_hash']
        data = python_object['data']
        nonce = int(python_object['nonce'])

        assert index == new_block.index
        assert cur_hash == new_block.hash
        assert prev_hash == new_block.prev_hash
        assert data == new_block.data
        assert nonce == new_block.nonce


def test_create_genesis():
    for i in range(5):
        genesis_block = block.create_genesis()

        assert genesis_block is not None
        assert type(genesis_block) == block.Block

        assert genesis_block.index == 0
        assert genesis_block.hash[-4:] == "0000"
        assert genesis_block.prev_hash == 'GENESIS'
        assert len(genesis_block.data) == 256


def test_data_gen():
    for i in range(5):
        new_block1 = block.Block(1, "gen_test", 0, None)
        assert len(new_block1.data) == 256
        new_block2 = block.Block(1, "gen_test", 0, None)
        assert len(new_block2.data) == 256
        assert new_block1.data != new_block2.data
