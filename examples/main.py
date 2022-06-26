from appdata import appdata
from datetime import datetime, timezone

# defaults to app_data
appdata.set_file_store("my_app_data_dir")

# defaults to kv_store
appdata.set_key_value_store("my_store")

appdata["last_login"] = datetime.utcnow().replace(tzinfo=timezone.utc)

with appdata.write("some_file.txt") as f:
    f.write("Mjello")
