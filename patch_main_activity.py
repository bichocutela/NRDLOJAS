import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("val fontScale by userPreferences.fontScale.collectAsState(initial = 1.0f)", 
    "val fontScale by userPreferences.fontScale.collectAsState(initial = 1.0f)\n            val appTheme by userPreferences.appTheme.collectAsState(initial = \"red\")")

content = content.replace("MyApplicationTheme {", "MyApplicationTheme(appTheme = appTheme) {")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
print("Patched MainActivity")
