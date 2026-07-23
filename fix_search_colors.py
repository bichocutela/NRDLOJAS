import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("com.example.ui.theme.BlueContainer", "MaterialTheme.colorScheme.primaryContainer")
content = content.replace("com.example.ui.theme.BlueText", "MaterialTheme.colorScheme.onPrimaryContainer")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
