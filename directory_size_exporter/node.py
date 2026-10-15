import os
import os.path
import time

class Node:
    FULL_NODE_LIMIT = 24 * 60 * 60

    def __init__(self, parent: "Node" | None, name: str) -> None:
        self.parent = parent
        self.name = name

        self._mtime = os.stat(self.path).st_mtime

    def update(self) -> None:
        raise NotImplementedError()

    def replace_child(self, child: str) -> None:
        raise NotImplementedError()

    @property
    def age(self) -> int:
        return time.time() - self.mtime

    @property
    def mtime(self) -> int:
        raise NotImplementedError()

    @property
    def size(self) -> int:
        raise NotImplementedError()

    @property
    def path(self) -> str:
        if self.parent is None:
            return self.name
        else:
            return os.path.join(self.parent.path, self.name)
