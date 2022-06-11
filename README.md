# Python App Data
The py-appdata aims to solve the issue of storing simple application data and accessing it in an easy way.

The core idea is to expose a simple interface that has two properties
 - A get/set interface to simple values
 - A simple way of saving and retrieving files from the application directory

## Get started
````python
from appdata import appdata
from datetime import datetime

# defaults to app_data
appdata.set_file_store("my_app_data_dir")

# defaults to kv_store
appdata.set_key_value_store("my_store")

appdata["last_login"] = datetime.now()

with appdata.write("some_file.txt") as f:
    f.write("Mjello")
````
