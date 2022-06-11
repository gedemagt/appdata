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

# class AppDirsProvider(AppDataDirProvider):
#
#     def __init__(self, app_dirs: AppDirs):
#         super().__init__()
#         self._app_dirs = app_dirs
#
#     def get_in_app_dir(self, path: str):
#         parent = Path(self._app_dirs.user_data_dir)
#         return parent / path


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
