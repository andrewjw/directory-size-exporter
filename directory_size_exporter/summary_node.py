import random
import os
import time

from .node import Node

class SummaryNode(Node):
    def __init__(self, parent: "Node" | None, name: str) -> None:
        super().__init__(parent, name)

        self._update()

    def update(self) -> None:
        if random.random() < 0.1:
            self._update()

        print(self.path, (time.time() - self.mtime))
        if (time.time() - self.mtime) > 24 * 60 * 60:
            self.parent.replace_child(self.name)

    def _update(self) -> None:
        self._mtime = os.stat(self.path).st_mtime

        size = 0
        for file in os.listdir(self.path):
            try:
                path = os.path.join(self.path, file)
                #if os.path.islink(path):
                #    size += len(path)
                #    continue
                #print(dirpath, file, os.stat(path).st_size)
                if os.path.islink(path):
                    stat = os.lstat(path)
                    size += stat.st_size
                    if self._mtime < stat.st_mtime:
                        self._mtime = stat.st_mtime
                elif os.path.isdir(path):
                    sn = SummaryNode(self, file)
                    size += sn.size
                    if self._mtime < sn.mtime:
                        self._mtime = sn.mtime
                else:
                    stat = os.stat(path)
                    size += stat.st_size
                    if self._mtime < stat.st_mtime:
                        self._mtime = stat.st_mtime
            except FileNotFoundError:
                pass

        self.__size = size

    @property
    def size(self) -> int:
        return self.__size

    @property
    def mtime(self) -> int:
        return self._mtime