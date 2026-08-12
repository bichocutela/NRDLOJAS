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

print("Number of docs:", len(documents))
codes = [doc.get("fields", {}).get("code", {}).get("stringValue", "") for doc in documents]
print("Number of codes:", len(codes))
print("Unique codes:", len(set(codes)))

# What if 'code' is not stored as stringValue?
for doc in documents:
    fields = doc.get("fields", {})
    if "code" not in fields:
        print("Missing code in doc:", doc.get("name"))
