import urllib.request
import json

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

diff = []
for doc in documents:
    doc_id = doc.get("name").split("/")[-1]
    code = doc.get("fields", {}).get("code", {}).get("stringValue", "")
    if doc_id != code:
        diff.append((doc_id, code))

print("Different ID vs Code:", diff)
