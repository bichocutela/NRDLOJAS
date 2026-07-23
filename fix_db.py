import re

with open("app/src/main/java/com/example/data/AppDatabase.kt", "r") as f:
    content = f.read()

content = content.replace("version = 2", "version = 3")

with open("app/src/main/java/com/example/data/AppDatabase.kt", "w") as f:
    f.write(content)
