import requests
import json

url = "https://kkayksyzksexoarpfxyj.supabase.co/storage/v1/object/list/nrdlojas-images"
data = {"prefix": "", "limit": 100, "offset": 0, "sortBy": {"column": "name", "order": "asc"}}
# We need authorization. Wait, the bucket is public!
# Public buckets allow listing without auth?
res = requests.post(url, json=data)
print(res.status_code, res.text)
