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


# The KeyValue object now acts as a proxy, and can be used
kv.last_login = datetime.utcnow().replace(tzinfo=timezone.utc)
