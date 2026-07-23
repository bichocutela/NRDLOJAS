import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Icons.Default.QrCode", "Icons.Default.CameraAlt")
content = content.replace("import androidx.compose.material.icons.filled.QrCode", "import androidx.compose.material.icons.filled.CameraAlt")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
