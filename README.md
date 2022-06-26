# Python App Data
The py-appdata aims to solve the issue of storing simple application data and accessing it in an easy way.

The core idea is to expose a simple interface that has two properties
 - A get/set interface to simple values
 - A simple way of saving and retrieving files from the application directory

## Stores
The `AppData` class provides an interface to two storage-abstractions: A file system and a key-value store. This lets
you easily save/retrieve files as well as setting/loading key/values which is a common app-data usage.

## Installation
````bash
pip install py-appdata
````

## Get started
````python
from appdata import appdata
from datetime import datetime, timezone

# defaults to app_data
appdata.set_file_store("my_app_data_dir")

# defaults to kv_store
appdata.set_key_value_store("my_store")

appdata["last_login"] = datetime.utcnow().replace(tzinfo=timezone.utc)

with appdata.write("some_file.txt") as f:
    f.write("Mjello")
````
## Auto save
The AppData object will auto save as a default. This means, whenever the KeyValue-store has been altered, it will 
automatically flush.
This can be disabled, but then you are in charge of flushing. This can either be via the context manager or directly
via the save method.
````python
from appdata import appdata

appdata.set_auto_save(False)

with appdata:
    appdata["kv1"] = "something"
    appdata["kv2"] = "something else"
    
# Or directly

appdata["kv3"] = "something completely else"
appdata.save()


````

## Dataclass support
If you like type hints, you can register a `dataclass` instance as a proxy for the key-value store
```python
from appdata import appdata
from datetime import datetime, timezone
from dataclasses import dataclass


# Define the dataclass
@dataclass
class KV:
    last_login: datetime = None


# Create an object to be referenced and register it to appdata
kv = KV()
appdata.register(kv)


# The KeyValue object now acts as a proxy, and can be used throughout your project
kv.last_login = datetime.utcnow().replace(tzinfo=timezone.utc)
```

## Custom KeyValue Store
You can create a custom KeyValue store by extending the `KeyValueStore` base class, or the `DictKeyValueStore` if you 
want to use a dict internally, and serialize it in a special way. Remember to registering it to the AppData object.
````python
from appdata import appdata
from appdata.kv_store import KeyValueStore

class MyKeyValueStore(KeyValueStore):
    
    ...


# defaults to app_data
appdata.set_key_value_store(MyKeyValueStore())
````

## Custom File Store
You can create a custom file store by extending the `FileStore` class and registering it to the AppData object
````python
from appdata import appdata
from appdata.file_store import FileStore

class MyFileStore(FileStore):
    
    ...


# defaults to app_data
appdata.set_file_store(MyFileStore())
````
