from pathlib import Path
from typing import Any, Union, IO

from appdata.file_store import FileStore, Directory
from appdata.store import KeyValueStore, PickleStore


class AppData:

    def __init__(self, key_value_store: Union[str, KeyValueStore] = "kv_store",
                 file_store: Union[str, FileStore] = "app_data",
                 auto_save=True
                 ):

        self._auto_save: bool = auto_save

        if isinstance(key_value_store, str):
            self._key_value_store = PickleStore(key_value_store)
        else:
            self._key_value_store = key_value_store

        self._file_store: FileStore = file_store
        if self._file_store:
            self.set_file_store(file_store)
            self._key_value_store.init(self._file_store)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def __setitem__(self, key: str, value: Any):
        self._key_value_store.set_item(key, value)
        if self._auto_save:
            self.save()

    def __getitem__(self, key: str):
        return self._key_value_store.get_item(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def save(self):
        if self._file_store:
            self._key_value_store.flush(self._file_store)

    def set_key_value_store(self, key_value_store: KeyValueStore):
        self._key_value_store = key_value_store
        if self._file_store:
            self._key_value_store.init(self._file_store)

    def set_file_store(self, file_store: Union[str, FileStore]):
        if isinstance(file_store, str):
            self._file_store = Directory(file_store)
        else:
            self._file_store = file_store

    def write(self, path: Union[str, Path]) -> IO:
        return self._file_store.file(path, 'w')

    def read(self, path: Union[str, Path]) -> IO:
        return self._file_store.file(path, 'r')

    def write_binary(self, path: Union[str, Path]) -> IO:
        return self._file_store.file(path, 'wb')

    def read_binary(self, path: Union[str, Path]) -> IO:
        return self._file_store.file(path, 'rb')

    def file(self, path: Union[str, Path], mode) -> IO:
        return self._file_store.file(path, mode)


appdata = AppData()
