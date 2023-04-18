from flask import Flask, request
import node
import threading
import logging
import requests
import time
import sys
from gevent import monkey

monkey.patch_all()
logging.getLogger('werkzeug').disabled = True


class Server:
    PEER_PORTS = {
        3001: [3002, 3003],
        3002: [3001, 3003],
        3003: [3001, 3002],
    }

    def __init__(self, port: int):
        self.id = port % 10  # Node ID
        self.port = port
        self.peer_ports = self.PEER_PORTS[self.port]
        self.received_block = False
        self.stop_event = False
        self.node = node.Node(self)

    def start(self):
        self.start_flask()
        self.start_block_generator()

    def start_flask(self):
        app = Flask(__name__)

        @app.route("/", methods=["POST"])
        def post_block():
            block = request.get_json()
            self.received_block = True
            try:
                self.node.handle_received_block(block)
                time.sleep(1)
                self.received_block = False
                return "Received new block"
            except Exception as e:
                logging.error(f"Exception: {e}")
                self.received_block = False
                return "Failed to receive the block"

        app_thread = threading.Thread(
            target=app.run, kwargs={"host": "localhost", "port": self.port}, daemon=True
        )
        app_thread.start()

    def block_generator(self):
        if self.id == 1 and not self.node.blocks:
            genesis_block = self.node.add_genesis()
            self.broadcast_block(genesis_block)
        if self.node.blocks:
            new_block = self.node.create_new_block()
            if not self.received_block:
                self.node.blocks.append(new_block)
                self.node.last_block = new_block
                self.broadcast_block(new_block)
        time.sleep(1)

    def start_block_generator(self):
        while not self.stop_event:
            self.block_generator()

    def broadcast_block(self, block):
        urls = [f"http://localhost:{p}/" for p in self.peer_ports]
        if not self.received_block:
            for url in urls:
                requests.post(url, json=block.to_json(self.id))

    def stop_thread(self):
        self.stop_event = True

    def start_limited_generator(self, length):
        for i in range(length):
            self.block_generator()


if __name__ == "__main__":
    this_port = int(sys.argv[1])
    server = Server(this_port)
    server.start()
