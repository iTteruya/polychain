from src.main import Server
import random
import pytest


@pytest.fixture
def three_servers():
    server3 = Server(3003)
    server2 = Server(3002)
    server1 = Server(3001)

    return server1, server2, server3


def test_server_init(three_servers):
    for i in range(5):
        server1, server2, server3 = three_servers

        assert server1.id == 1
        assert server2.id == 2
        assert server3.id == 3

        assert server1.peer_ports == [3002, 3003]
        assert server2.peer_ports == [3001, 3003]
        assert server3.peer_ports == [3001, 3002]


def test_start_and_generator(three_servers):
    server1, server2, server3 = three_servers

    server1.local = True
    server2.local = True
    server3.local = True

    server3.start_flask()
    server2.start_flask()
    server1.start_flask()

    assert server3.stop_event is False
    assert server2.stop_event is False
    assert server1.stop_event is False

    length = random.randint(1, 5)
    server1.start_limited_generator(length)

    assert len(server1.node.blocks) == length + 1
    assert len(server2.node.blocks) == length + 1
    assert len(server3.node.blocks) == length + 1

    assert server1.node.blocks[0].prev_hash == 'GENESIS'
    assert server2.node.blocks[0].prev_hash == 'GENESIS'
    assert server3.node.blocks[0].prev_hash == 'GENESIS'

    for i in range(1, length):
        assert server1.node.blocks[i].hash == server2.node.blocks[i].hash == server3.node.blocks[i].hash
        assert server1.node.blocks[i].prev_hash == server2.node.blocks[i - 1].hash == server3.node.blocks[i - 1].hash
        assert server1.node.blocks[i].data == server2.node.blocks[i].data == server3.node.blocks[i].data
        assert server1.node.blocks[i].timestamp == server2.node.blocks[i].timestamp == server3.node.blocks[i].timestamp
        assert server1.node.blocks[i].index == i
        assert server2.node.blocks[i].index == i
        assert server3.node.blocks[i].index == i

    server3.stop_thread()
    server2.stop_thread()
    server1.stop_thread()

    assert server3.stop_event is True
    assert server2.stop_event is True
    assert server1.stop_event is True
