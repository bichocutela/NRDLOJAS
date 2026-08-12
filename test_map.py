import urllib.request
import json
import collections

base_url = "https://firestore.googleapis.com/v1/projects/appcodigo-7f245/databases/(default)/documents/products"
req = urllib.request.Request(base_url + "?pageSize=5")
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode('utf-8'))
    for doc in data.get("documents", []):
        print(doc.get("fields", {}).get("code", {}).get("stringValue", ""))
