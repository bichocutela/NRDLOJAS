import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = content.replace("dependencies {", 'dependencies {\n  implementation("com.google.zxing:core:3.5.3")')

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
