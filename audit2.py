import urllib.request
import json
import collections

base_url = "https://firestore.googleapis.com/v1/projects/appcodigo-7f245/databases/(default)/documents/products"
next_page_token = None
documents = []

while True:
    url = base_url + "?pageSize=300"
    if next_page_token:
        url += f"&pageToken={next_page_token}"
    
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        docs = data.get("documents", [])
        documents.extend(docs)
        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

code_map = collections.defaultdict(list)

for doc in documents:
    fields = doc.get("fields", {})
    code = fields.get("code", {}).get("stringValue", "").strip()
    name = fields.get("name", {}).get("stringValue", "")
    category = fields.get("category", {}).get("stringValue", "")
    doc_name = doc.get("name", "")
    doc_id = doc_name.split("/")[-1]
    
    code_map[code].append({
        "name": name,
        "category": category,
        "id": doc_id
    })

duplicates = {k: v for k, v in code_map.items() if len(v) > 1}
print(f"TOTAL: {len(documents)}")
print(f"DUPES: {len(duplicates)}")
