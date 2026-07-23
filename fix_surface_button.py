import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("import androidx.compose.material3.SurfaceButton", "import androidx.compose.material3.TextButton")
content = content.replace("import androidx.compose.material3.Text\\nimport androidx.compose.material3.Surface", "import androidx.compose.material3.Text\\nimport androidx.compose.material3.Surface") # wait

# clean up duplicate Text
content = re.sub(r'import androidx\.compose\.material3\.Text\n(.*)import androidx\.compose\.material3\.Text\n', r'import androidx.compose.material3.Text\n\1', content, flags=re.DOTALL)


with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
