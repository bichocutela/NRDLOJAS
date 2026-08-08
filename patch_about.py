import sys

with open("app/src/main/java/com/example/ui/AboutScreen.kt", "r") as f:
    content = f.read()

target = "Versão: 1.0\\n"
replacement = "Versão: ${com.example.BuildConfig.VERSION_NAME}\\n"

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/AboutScreen.kt", "w") as f:
        f.write(content)
    print("Patched AboutScreen successfully.")
else:
    print("Target not found in AboutScreen.")
