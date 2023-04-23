import random
from src.block import create_genesis
from src.node import Node
from src.main import Server
import pytest


def test_add_genesis():
    for i in range(5):
        node = Node(1)
        genesis = node.add_genesis()
        assert len(node.blocks) == 1
        assert node.last_block == genesis and node.last_block is not None
        assert node.blocks[0].index == 0 and node.blocks[0].prev_hash == "GENESIS"
        assert node.last_block == node.blocks[-1]


@pytest.mark.parametrize('server_id', [3001, 3002, 3003])
def test_create_new_block(server_id):
    server = Server(server_id)
    server.node.add_genesis()
    for i in range(5):
        block = server.node.create_new_block()
        server.node.blocks.append(block)
        server.node.last_block = block

    for i in range(1, len(server.node.blocks)):
        current_block = server.node.blocks[i]
        prev_block = server.node.blocks[i - 1]
        current_block_hash = server.node.blocks[i].hash

        assert current_block.hash == current_block_hash
        assert prev_block.hash == current_block.prev_hash


@pytest.mark.parametrize('server_id', [3001, 3002, 3003])
def test_handle_received_block(server_id):
    server = Server(server_id)
    genesis = create_genesis().to_json(server.id)
    res = server.node.handle_received_block(genesis)

    assert len(server.node.blocks) == 1 and server.node.last_block is not None
    assert res is True

    ports = [3001, 3002, 3003]
    for i in range(5):
        port = random.choice(ports)
        new_block = server.node.create_new_block()
        if port == server_id:
            server.node.blocks.append(new_block)
            server.node.last_block = new_block
        else:
            block_to_json = new_block.to_json(port)
            res = server.node.handle_received_block(block_to_json)

            assert server.node.blocks[i + 1].to_json(0) == new_block.to_json(0)
            assert server.node.last_block.to_json(0) == new_block.to_json(0)
            assert res is True

    assert server.node.is_valid()
