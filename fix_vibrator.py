import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("as Vibrator }", "as? Vibrator }")
content = content.replace("vibrator.vibrate", "vibrator?.vibrate")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
