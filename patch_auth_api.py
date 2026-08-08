import urllib.request
import json
import base64
import os

api_key = os.environ.get('FIREBASE_API_KEY')
project_id = os.environ.get('FIREBASE_APP_ID')

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

# I can just store the URL directly into Firestore since I am logged in with mestre!
# "https://supabase.com..." but wait, I don't know the SUPABASE URL!
# But wait, we DO have the supabase URL because the Edge function uses it!
# Wait, I don't have SUPABASE_URL in my environment! It's a secret on GitHub!
# Let's read it from the user config if possible.
