import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# find duplicate import and remove it
content = re.sub(r'import androidx\.compose\.ui\.layout\.ContentScale\n(.*)import androidx\.compose\.ui\.layout\.ContentScale\n', r'import androidx.compose.ui.layout.ContentScale\n\1', content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
