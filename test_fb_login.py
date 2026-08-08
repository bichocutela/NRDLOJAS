import urllib.request
import os
import json

api_key = os.environ.get('FIREBASE_API_KEY')
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
data = json.dumps({
    "email": "mestre@nrdlojas.com",
    "password": "nrdlojas",
    "returnSecureToken": True
}).encode('utf-8')

req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode('utf-8'))
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))
