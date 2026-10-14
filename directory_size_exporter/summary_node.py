import os

from .node import Node

class SummaryNode(Node):
    def __init__(self, parent: "Node" | None, name: str) -> None:
        super().__init__(parent, name)

        size = 0
        for file in os.listdir(self.path):
            try:
                path = os.path.join(self.path, file)
                #if os.path.islink(path):
                #    size += len(path)
                #    continue
                #print(dirpath, file, os.stat(path).st_size)
                if os.path.islink(path):
                    size += os.lstat(path).st_size
                elif os.path.isdir(path):
                    sn = SummaryNode(self, file)
                    size += sn.size
                else:
                    size += os.stat(path).st_size
            except FileNotFoundError:
                pass

        self.__size = size

    @property
    def size(self) -> int:
        return self.__size
