import os
import os.path

class Node:
    def __init__(self, parent: "Node" | None, name: str) -> None:
        self.parent = parent
        self.name = name

        self._mtime = os.stat(self.path).st_mtime

    def update(self) -> None:
        raise NotImplementedError()

    def replace_child(self, child: str) -> None:
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
