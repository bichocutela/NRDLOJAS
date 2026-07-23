import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Fix conflicting TextAlign imports
content = re.sub(r'import androidx\.compose\.ui\.text\.style\.TextAlign\n(.*)import androidx\.compose\.ui\.text\.style\.TextAlign\n', r'import androidx.compose.ui.text.style.TextAlign\n\1', content, flags=re.DOTALL)

# Also ensure Surface is imported from material3
if "import androidx.compose.material3.Surface" not in content:
    content = content.replace("import androidx.compose.material3.Text", "import androidx.compose.material3.Text\nimport androidx.compose.material3.Surface")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
