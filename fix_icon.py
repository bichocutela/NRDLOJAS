import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Icons.Default.QrCodeScanner", "Icons.Default.QrCode")
content = content.replace("import androidx.compose.material.icons.filled.QrCodeScanner", "import androidx.compose.material.icons.filled.QrCode")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
