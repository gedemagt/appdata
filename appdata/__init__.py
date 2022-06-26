from dataclasses import is_dataclass
from pathlib import Path
from typing import Any, Union, IO

from appdata.file_store import FileStore, Directory
from appdata.kv_store import KeyValueStore, JsonKVStore


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

    def register(self, _kv_object) -> None:
        """
        Registers a dataclass object as a key-value proxy
        :param _kv_object: A dataclass object
        """

        if not is_dataclass(_kv_object):
            raise ValueError("Please use dataclass object.")

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

    def __delitem__(self, key):
        self._key_value_store.delete_item(key)
        if self._auto_save:
            self.save()

    def get(self, key: str, default=None) -> Any:
        """
        Get the application data object of some key. If it doesn't exists,
        return the default parameter.
        :param key: The key
        :param default: A default parameter if the key doesn't exits
        :return: The app data value or the default
        """
        try:
            return self[key]
        except KeyError:
            return default

    def save(self) -> None:
        """
        Flushes the KeyValue store
        """
        if self._file_store:
            self._key_value_store.flush(self._file_store)

    def set_key_value_store(self, key_value_store: Union[KeyValueStore]):
        """
        Set a new KeyValue store. If the parameters is a string, a JsonKVStore
        is constructed with the value as the name of the file.
        :param key_value_store: A str or a KeyValueStore object.
        """
        if isinstance(key_value_store, str):
            self._key_value_store = JsonKVStore(key_value_store)
        else:
            self._key_value_store = key_value_store

        if self._file_store:
            self._key_value_store.init(self._file_store)

    def set_file_store(self, file_store: Union[str, FileStore]):
        """
        Set a new file store. If the parameters is a string, a DirectoryStore
        is constructed with the value as the path to the directory.
        :param file_store: A str or a FileStore object.
        """
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
        """
        Returns a file-like object in a given mode.
        :param path: The path to the file in the file store
        :param mode: The mode - same as open()
        :return: A file-like object
        """
        return self._file_store.file(path, mode)

    def set_auto_save(self, auto_save: bool) -> None:
        """
        Sets the auto save on or off
        :param auto_save: Value of auto-save
        """
        self._auto_save = auto_save


appdata = AppData()
