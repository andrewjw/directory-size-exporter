import os

class Directory:
    def __init__(self, path: str) -> None:
        self.path = path

        stat = os.stat(path)

        self.atime = stat.st_atime
        self.files_size = 0
        self.recursive_size = 0

    def update(self) -> None:
