import re

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    content = f.read()

# Remove signInAnonymously()
pattern_init = re.compile(r'fun initialize\(context: android\.content\.Context\) \{[\s\S]*?\} catch \(e: Exception\) \{[\s\S]*?\}\s*\}')
replacement_init = '''fun initialize(context: android.content.Context) {
        // Inicialização removida conforme solicitado (não usar signInAnonymously).
    }'''

content = pattern_init.sub(replacement_init, content)

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
    f.write(content)
print("Patched FirebaseService to remove signInAnonymously")
