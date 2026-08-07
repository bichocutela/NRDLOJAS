with open("app/src/main/java/com/example/data/FirebaseService.kt", "r") as f:
    content = f.read()

import re

new_content = re.sub(r'lastError = "Chaves do Firebase.*', 'lastError = "API_KEY=" + (if(rawApiKey=="dummy") "FALTA" else "OK") + ", PROJ=" + (if(rawProjectId=="dummy") "FALTA" else "OK") + ", APP=" + (if(rawAppId=="dummy") "FALTA" else "OK")', content)

with open("app/src/main/java/com/example/data/FirebaseService.kt", "w") as f:
    f.write(new_content)
