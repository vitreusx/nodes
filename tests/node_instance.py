from noded import Node
from multiprocessing import Process

class NodeInstance:
    def __init__(self, *args, **kwargs):
        def node_thread_fn():
            node = Node(*args, *kwargs)
            node.run()

        self.node_process = Process(target = node_thread_fn)
        self.node_process.start()

    def __del__(self):
        self.node_process.terminate()
