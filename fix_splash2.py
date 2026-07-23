import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("R.drawable.logo_nordestao", "R.drawable.splash_logo")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
