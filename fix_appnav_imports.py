with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

if "import androidx.compose.runtime.getValue" not in content:
    content = content.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\nimport androidx.compose.runtime.getValue")

if "import androidx.compose.runtime.collectAsState" not in content:
    content = content.replace("import androidx.compose.runtime.Composable", "import androidx.compose.runtime.Composable\nimport androidx.compose.runtime.collectAsState")

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/ManageTabsScreen.kt", "r") as f:
    content = f.read()
if "import androidx.compose.runtime.getValue" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue")
with open("app/src/main/java/com/example/ui/ManageTabsScreen.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/ManageProductsScreen.kt", "r") as f:
    content = f.read()
if "import androidx.compose.runtime.getValue" not in content:
    content = content.replace("import androidx.compose.runtime.*", "import androidx.compose.runtime.*\nimport androidx.compose.runtime.getValue\nimport androidx.compose.runtime.setValue")
with open("app/src/main/java/com/example/ui/ManageProductsScreen.kt", "w") as f:
    f.write(content)
