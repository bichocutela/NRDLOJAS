import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun StylizedText", "@Composable\nfun StylizedText")

content = content.replace("@Composable\nfun SearchScreen", "@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun SearchScreen")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
