import re
import os

files_to_fix = [
    "app/src/main/java/com/example/ui/ManageTabsScreen.kt",
    "app/src/main/java/com/example/ui/ManageProductsScreen.kt"
]

for file in files_to_fix:
    if os.path.exists(file):
        with open(file, "r") as f:
            content = f.read()
        if "import androidx.compose.runtime.collectAsState" not in content:
            content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.runtime.collectAsState")
        with open(file, "w") as f:
            f.write(content)
