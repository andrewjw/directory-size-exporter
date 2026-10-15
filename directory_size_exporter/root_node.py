import os
import time

from .node import Node
from .full_node import FullNode
from .summary_node import SummaryNode

class RootNode(Node):
    def __init__(self, path: str) -> None:
        self.node: Node = self._get_node_for_directory(path, os.stat(path).st_mtime)

    def update(self) -> None:
        self.node.update()

    def replace_child(self, path: str) -> None:
        self.node = self._get_node_for_directory(path, self.node.mtime)

    def _get_node_for_directory(self, path: str, mtime: int) -> Node:
        if (time.time() - mtime) > self.FULL_NODE_LIMIT:
            print("Get summary for ", path, mtime, time.time() - mtime)
            return SummaryNode(self, path)
        else:
            print("Get full for ", path, mtime, time.time() - mtime)
            return FullNode(self, path)

    @property
    def size(self) -> int:
        return self.node.size

    @property
    def path(self) -> str:
        return ""
