import sys

with open("app/src/main/java/com/example/ui/AboutScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport androidx.compose.ui.Alignment\nimport androidx.compose.ui.graphics.asImageBitmap")

with open("app/src/main/java/com/example/ui/AboutScreen.kt", "w") as f:
    f.write(content)
