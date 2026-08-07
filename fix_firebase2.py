import sys

with open("app/src/main/java/com/example/data/FirebaseService.kt", "r") as f:
    lines = f.readlines()

new_lines = []
inside_init = False
for line in lines:
    if "fun initialize(context: android.content.Context)" in line:
        inside_init = True
        new_lines.append(line)
        new_lines.append("""        try {
            FirebaseApp.getInstance()
            try {
                val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
                if (auth.currentUser == null) {
                    auth.signInAnonymously()
                }
            } catch (e: Exception) {
            }
        } catch (e: Exception) {
            val rawApiKey = com.example.BuildConfig.FIREBASE_API_KEY
            val rawProjectId = com.example.BuildConfig.FIREBASE_PROJECT_ID
            val rawAppId = com.example.BuildConfig.FIREBASE_APP_ID
                        
            if (rawApiKey != "dummy" && rawProjectId != "dummy" && rawAppId != "dummy") {
                val apiKey = rawApiKey
                val appId = if (rawProjectId.contains(":") && !rawAppId.contains(":")) rawProjectId else rawAppId
                val projectId = if (rawProjectId.contains(":") && !rawAppId.contains(":")) rawAppId else rawProjectId
                
                try {
                    val options = com.google.firebase.FirebaseOptions.Builder()
                        .setApiKey(apiKey)
                        .setProjectId(projectId)
                        .setApplicationId(appId)
                        .setStorageBucket(projectId + ".appspot.com")
                        .build()
                    FirebaseApp.initializeApp(context, options)
                    
                    try {
                        com.google.firebase.auth.FirebaseAuth.getInstance().signInAnonymously()
                    } catch (e: Exception) {
                        Log.e("FirebaseService", "Auth error", e)
                    }
                } catch (ex: Exception) {
                    lastError = "Init error: " + ex.message
                    Log.e("FirebaseService", "Erro ao inicializar Firebase", ex)
                }
            } else {
                lastError = "API_KEY=${if (rawApiKey=="dummy") "FALTA" else "OK"}, PROJECT=${if (rawProjectId=="dummy") "FALTA" else "OK"}, APP_ID=${if (rawAppId=="dummy") "FALTA" else "OK"}"
            }
        }
    }
""")
        continue
    
    if inside_init:
        if "suspend fun uploadBanner" in line:
            inside_init = False
            new_lines.append(line)
        continue
    
    if not inside_init:
        new_lines.append(line)

with open("app/src/main/java/com/example/data/FirebaseService.kt", "w") as f:
    f.writelines(new_lines)
