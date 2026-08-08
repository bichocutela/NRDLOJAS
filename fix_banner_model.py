import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace('"$supabaseUrl/storage/v1/object/public/nrdlojas-images/banners/themes/theme_red.jpg"', 'null')

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
print("Fixed bannerModel fallback for red theme.")
