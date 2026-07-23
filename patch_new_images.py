import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("R.drawable.splash_logo", "R.drawable.splash_logo_new")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content2 = f.read()

content2 = content2.replace("R.drawable.hero_banner", "R.drawable.hero_banner_new")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content2)

