import os
import requests

supabase_url = "https://kkayksyzksexoarpfxyj.supabase.co"

url = f"{supabase_url}/storage/v1/bucket"
print(requests.get(url).text)

url = f"{supabase_url}/storage/v1/object/list/nrdlojas-images"
data = {"prefix": "banners/", "limit": 100, "offset": 0, "sortBy": {"column": "name", "order": "asc"}}
res = requests.post(url, json=data)
print(res.text)

data = {"prefix": "banners/themes/", "limit": 100, "offset": 0, "sortBy": {"column": "name", "order": "asc"}}
res = requests.post(url, json=data)
print(res.text)

