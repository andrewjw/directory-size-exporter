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

        if (time.time() - self.mtime) < self.FULL_NODE_LIMIT:
            self.parent.replace_child(self.name)

    def _update(self) -> None:
        self._mtime = os.stat(self.path).st_mtime

        size, files, dirs = 0, 0, 0
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
                    dirs += 1 + sn.dir_count
                    files += sn.file_count
                    if self._mtime < sn.mtime:
                        self._mtime = sn.mtime
                else:
                    stat = os.stat(path)
                    size += stat.st_size
                    files += 1
                    if self._mtime < stat.st_mtime:
                        self._mtime = stat.st_mtime
            except FileNotFoundError:
                pass

        self.__size = size
        self.__dirs = dirs
        self.__files = files

    @property
    def size(self) -> int:
        return self.__size

    @property
    def file_count(self) -> int:
        return self.__files

    @property
    def dir_count(self):
        return self.__dirs

    @property
    def mtime(self) -> int:
        return self._mtime
