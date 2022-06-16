import os.path
from abc import ABC, abstractmethod
from pathlib import Path

from typing import Union, IO


class FileStore(ABC):

    @abstractmethod
    def exists(self, path: Union[str, Path]):
        pass

    @abstractmethod
    def file(self, path: Union[str, Path], mode='r') -> IO:
        pass


class Directory(FileStore):

    def __init__(self, path):
        self._parent = Path(path)

    def _to_path(self, path):
        return self._parent / path

    def exists(self, path: Union[str, Path]):
        return os.path.exists(self._parent / path)

    def file(self, path: Path, mode='r') -> IO:
        path = self._parent / path
        if 'w' in mode:
            path.parent.mkdir(parents=True, exist_ok=True)
        return open(path, mode)

    def __str__(self):
        return f"DirectoryStore<path={self._parent}>"
