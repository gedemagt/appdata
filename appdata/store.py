import pickle

from abc import ABC, abstractmethod
from typing import Any

from appdata import FileStore


class KeyValueStore(ABC):

    @abstractmethod
    def flush(self, file_store: FileStore):
        pass

    @abstractmethod
    def init(self, file_store: FileStore):
        pass

    @abstractmethod
    def set_item(self, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_item(self, key: str) -> Any:
        pass


class PickleStore(KeyValueStore):

    def __init__(self, path):
        super().__init__()
        self._path = path
        self._internal = {}

    def flush(self, file_store: FileStore) -> None:
        with file_store.file(self._path, 'wb') as f:
            pickle.dump(self._internal, f, protocol=pickle.HIGHEST_PROTOCOL)

    def init(self, file_store: FileStore) -> None:

        try:
            with file_store.file(self._path, 'rb') as f:
                self._internal = pickle.load(f)
        except FileNotFoundError:
            pass

    def set_item(self, key: str, value: Any) -> None:
        self._internal[key] = value

    def get_item(self, key: str) -> Any:
        return self._internal[key]
