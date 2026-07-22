import re
with open("app/build.gradle.kts", "r") as f:
    content = f.read()

replacement = """    create("debugConfig") {
      storeFile = file("${rootDir}/debug.keystore")
      storePassword = "android"
      keyAlias = "androiddebugkey"
      keyPassword = "android"
    }"""

content = re.sub(r'    create\("debugConfig"\)\s*\{[^\}]*\}[^\}]*\}', replacement, content)

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
