import re

with open("app/src/main/res/drawable/ic_launcher_foreground.xml", "r") as f:
    content = f.read()

content = content.replace("@drawable/logo_nordestao", "@drawable/app_icon")

with open("app/src/main/res/drawable/ic_launcher_foreground.xml", "w") as f:
    f.write(content)
