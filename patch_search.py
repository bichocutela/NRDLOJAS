import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

image_code = """
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.primary)
            )
"""

content = re.sub(r'Image\(\s*painter\s*=\s*painterResource\(id\s*=\s*R\.drawable\.hero_banner\),\s*contentDescription\s*=\s*"Banner Nordestão",\s*contentScale\s*=\s*ContentScale\.Crop,\s*modifier\s*=\s*Modifier\.fillMaxSize\(\)\s*\)', image_code.strip(), content)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
