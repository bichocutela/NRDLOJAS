import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# remove all ContentScale imports
content = content.replace("import androidx.compose.ui.layout.ContentScale\n", "")

# add it back once at the top
content = content.replace("package com.example.ui", "package com.example.ui\nimport androidx.compose.ui.layout.ContentScale")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
