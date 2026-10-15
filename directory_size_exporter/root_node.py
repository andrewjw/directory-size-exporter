import os
import time

from .node import Node
from .full_node import FullNode
from .summary_node import SummaryNode

class RootNode(Node):
    def __init__(self, path: str) -> None:
        self.node: Node = self._get_node_for_directory(path)

    def update(self) -> None:
        self.node.update()

    def replace_child(self, path: str) -> None:
        self.node = self._get_node_for_directory(path)

    def _get_node_for_directory(self, path) -> Node:
        if (time.time() - os.stat(path).st_mtime) > 24 * 60 * 60:
            print("Get summary for ", path)
            return SummaryNode(self, path)
        else:
            print("Get full for ", path)
            return FullNode(self, path)

    @property
    def size(self) -> int:
        return self.node.size

    @property
    def path(self) -> str:
        return ""
