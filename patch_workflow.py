with open(".github/workflows/upload_theme_banners.yml", "r") as f:
    content = f.read()

content = content.replace("app/src/main/res/drawable-nodpi/", "app/src/main/assets/themes/")

with open(".github/workflows/upload_theme_banners.yml", "w") as f:
    f.write(content)
