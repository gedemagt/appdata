# Python App Data
The py-appdata aims to solve the issue of storing simple application data and accessing it in an easy way.

The core idea is to expose a simple interface that has two properties
 - A get/set interface to simple values
 - A simple way of saving and retrieving files from the application directory

## Stores
The `AppData` class provides an interface to two storage-abstractions: A file system and a key-value store. This lets
you easily save/retrieve files as well as setting/loading key/values which is a common app-data usage.

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