import os
import os.path
import time
from typing import Set

from .root_node import RootNode

class TopLevel:
    def __init__(self, root: str, level: int) -> None:
        self.root = root
        self.level = level

        self.roots = {}

    def update(self) -> None:
        roots = self._get_roots(self.root, self.level)

        for missing in set(self.roots.keys()) - roots:
            del self.roots[missing]

        for added in roots - set(self.roots.keys()):
            self.roots[added] = RootNode(added)

        for node in self.roots.values():
            start = time.time()
            node.update()
            size, files, dirs = node.size, node.file_count, node.dir_count
            end = time.time()
            print(node.node.path, size, files, dirs, end - start)

    def _get_roots(self, root, level) -> Set[str]:
        if level == 0:
            return set([root])

        roots = []
        for fn in os.listdir(root):
            if os.path.isdir(fn):
                roots.extend(self._get_roots(fn, level - 1))
        return set(roots)
