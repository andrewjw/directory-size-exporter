import os
import time
import threading
from typing import Dict

from .node import Node
from .summary_node import SummaryNode

class FullNode(Node):
    def __init__(self, parent: "Node" | None, name: str) -> None:
        super().__init__(parent, name)

        self.__lock = threading.RLock()
        self._mtime = os.stat(self.path).st_mtime
        self.children: Dict[str, Node] = {}
        self.files: Dict[str, (int, int)] = {}

        for file in os.listdir(self.path):
            self._update_child(file)

    def update(self) -> None:
        with self.__lock:
            new_dir = os.listdir(self.path)

            for file in new_dir:
                self._update_child(file)

            for deleted in (set(self.files.keys()) | set(self.children.keys())) - set(new_dir):
                if deleted in self.files:
                    del self.files[deleted]
                if deleted in self.children:
                    del self.children[deleted]

            if self.age > self.FULL_NODE_LIMIT:
                return self.parent.replace_child(self.name) 

    def replace_child(self, file: str) -> None:
        self.children[file] = self._get_node_for_directory(file)

    def _get_node_for_directory(self, path) -> Node:
        if path in self.children:
            if (time.time() - self.children[path].mtime) > self.FULL_NODE_LIMIT:
                return SummaryNode(self, path)
            else:
                return FullNode(self, path)
        else:
            return SummaryNode(self, path)

    def _update_child(self, file) -> None:
        try:
            path = os.path.join(self.path, file)

            if os.path.islink(path):
                stat = os.lstat(path).st_size
                self.files[file] = stat.st_size, stat.st_mtime
                if file in self.children:
                    del self.children[file]
            elif os.path.isdir(path):
                if file in self.children:
                    self.children[file].update()
                else:
                    self.children[file] = self._get_node_for_directory(file)
                if file in self.files:
                    del self.files[file]
            else:
                stat = os.stat(path)
                self.files[file] = stat.st_size, stat.st_mtime
                if file in self.children:
                    del self.children[file]
        except FileNotFoundError:
            pass

    @property
    def size(self) -> int:
        return sum([v[0] for v in self.files.values()]) + sum([n.size for n in self.children.values()])

    @property
    def file_count(self) -> int:
        return len(self.files) + sum([n.file_count for n in self.children.values()])

    @property
    def dir_count(self):
        return len(self.children) + sum([n.dir_count for n in self.children.values()])

    @property
    def mtime(self) -> int:
        return max([self._mtime] + [v[1] for v in self.files.values()] + [n.mtime for n in self.children.values()])
