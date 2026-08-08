import urllib.request
import os
import json
import base64

# 1. Login
api_key = os.environ.get('FIREBASE_API_KEY')
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
data = json.dumps({
    "email": "mestre@nrdlojas.com",
    "password": "nrdlojas",
    "returnSecureToken": True
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
id_token = None
try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        id_token = res.get('idToken')
except Exception as e:
    print("Error in login:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
    exit(1)

# 2. Upload image via Supabase Edge Function
supabase_url = os.environ.get('SUPABASE_URL')
upload_url = f"{supabase_url}/functions/v1/upload-image"

# Read image
image_path = "/app/applet/app/src/main/res/drawable-nodpi/hero_banner.png"
with open(image_path, "rb") as f:
    image_data = f.read()

import uuid
boundary = uuid.uuid4().hex

body = bytearray()
body.extend(f"--{boundary}\r\n".encode('utf-8'))
body.extend(b"Content-Disposition: form-data; name=\"path\"\r\n\r\n")
body.extend(b"banners/home_banner.png\r\n")

body.extend(f"--{boundary}\r\n".encode('utf-8'))
body.extend(b"Content-Disposition: form-data; name=\"file\"; filename=\"home_banner.png\"\r\n")
body.extend(b"Content-Type: image/png\r\n\r\n")
body.extend(image_data)
body.extend(b"\r\n")
body.extend(f"--{boundary}--\r\n".encode('utf-8'))

req_upload = urllib.request.Request(upload_url, data=body)
req_upload.add_header('Authorization', f"Bearer {os.environ.get('SUPABASE_ANON_KEY')}")
req_upload.add_header('x-firebase-token', id_token)
req_upload.add_header('Content-Type', f"multipart/form-data; boundary={boundary}")

public_url = None
try:
    with urllib.request.urlopen(req_upload) as response:
        res = json.loads(response.read().decode('utf-8'))
        public_url = res.get('url')
        print("Upload success:", public_url)
except Exception as e:
    print("Error in upload:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
    exit(1)

# 3. Save to Firestore
if public_url:
    firestore_url = f"https://firestore.googleapis.com/v1/projects/{os.environ.get('FIREBASE_PROJECT_ID')}/databases/(default)/documents/config/appSettings"
    
    update_data = json.dumps({
        "fields": {
            "bannerUrl": {
                "stringValue": public_url
            }
        }
    }).encode('utf-8')
    
    # We use PATCH to upsert the document
    patch_url = f"{firestore_url}?updateMask.fieldPaths=bannerUrl"
    req_fs = urllib.request.Request(patch_url, data=update_data, method='PATCH')
    req_fs.add_header('Authorization', f"Bearer {id_token}")
    req_fs.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(req_fs) as response:
            print("Firestore update success:", response.read().decode('utf-8'))
    except Exception as e:
        print("Error in Firestore update:", e)
        if hasattr(e, 'read'):
            print(e.read().decode('utf-8'))
