with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    lines = f.readlines()

start = -1
end = -1
for i, line in enumerate(lines):
    if line.startswith('    fun initialize(context:'):
        start = i
    if line.startswith('    suspend fun uploadBanner(context:'):
        end = i

if start != -1 and end != -1:
    new_lines = lines[:start] + [
        '    fun initialize(context: android.content.Context) {\n',
        '        try {\n',
        '            val auth = com.google.firebase.auth.FirebaseAuth.getInstance()\n',
        '            if (auth.currentUser == null) {\n',
        '                auth.signInAnonymously()\n',
        '            }\n',
        '        } catch (e: Exception) {\n',
        '            Log.e("FirebaseService", "Auth error", e)\n',
        '        }\n',
        '    }\n',
        '\n'
    ] + lines[end:]
    
    with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
        f.writelines(new_lines)
