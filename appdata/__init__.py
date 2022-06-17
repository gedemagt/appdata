from pathlib import Path
from typing import Any, Union, IO

from appdata.file_store import FileStore, Directory
from appdata.kv_store import KeyValueStore, PickleStore, JsonKVStore


class AppData:

    def __init__(self, key_value_store: Union[str, KeyValueStore] = "kv_store",
                 file_store: Union[str, FileStore] = "app_data",
                 auto_save=True
                 ):

        self._auto_save: bool = auto_save

        self._key_value_store: KeyValueStore = None
        self._file_store: FileStore = None

        self.set_file_store(file_store)
        self.set_key_value_store(key_value_store)

        self._kv_object = None

    def register(self, _kv_object):
        self._kv_object = _kv_object
        for key, val in self._key_value_store.get_all().items():
            setattr(_kv_object, key, val)

        def method(self, name, value, callback=self._set_to_store):
            callback(name, value)
            super(self.__class__, self).__setattr__(name, value)

        meths = {'__setattr__': method}
        _kv_object.__class__ = type('KV', (_kv_object.__class__,), meths)

    def _set_to_store(self, key, value):
        self._key_value_store.set_item(key, value)
        if self._auto_save:
            self.save()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()

    def __setitem__(self, key: str, value: Any):
        if self._kv_object is not None:
            setattr(self._kv_object, key, value)
        self._set_to_store(key, value)

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
        if isinstance(key_value_store, str):
            self._key_value_store = JsonKVStore(key_value_store)
        else:
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
