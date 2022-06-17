import datetime
import json
import pickle

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Union, Dict

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

    @abstractmethod
    def get_all(self) -> Dict:
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

    def get_all(self) -> Dict:
        return self._internal.copy()


class JsonKVStore(KeyValueStore):

    def __init__(self, path: Union[str, Path]):
        self._path = path
        self._internal = {}

    def flush(self, file_store: FileStore):
        with file_store.file(self._path, 'w') as f:
            json.dump(self._internal, f, cls=_CustomEncoder)

    def init(self, file_store: FileStore):

        try:
            with file_store.file(self._path, 'r') as f:
                self._internal = json.load(f, object_hook=decode)
        except FileNotFoundError:
            pass

    def set_item(self, key: str, value: Any) -> None:
        self._internal[key] = value

    def get_item(self, key: str) -> Any:
        return self._internal[key]

    def get_all(self) -> Dict:
        return self._internal.copy()


class _CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return dict(type="__datetime__", value=obj.isoformat())

        return super(_CustomEncoder, self).default(obj)


def decode(dct):
    if isinstance(dct, dict):
        if dct.get('type') == "__datetime__":
            return datetime.datetime.fromisoformat(dct["value"])
    return dct
