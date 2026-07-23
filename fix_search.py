import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\n\n@Composable", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
