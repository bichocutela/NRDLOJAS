import re

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'    fun initialize\(context: android\.content\.Context\)\s*\{.*?    \}', re.DOTALL)

replacement = """    fun initialize(context: android.content.Context) {
        try {
            val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
            if (auth.currentUser == null) {
                auth.signInAnonymously()
            }
        } catch (e: Exception) {
            Log.e("FirebaseService", "Auth error", e)
        }
    }"""

new_content = pattern.sub(replacement, content, count=1)

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
    f.write(new_content)
