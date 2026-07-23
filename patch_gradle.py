import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = content.replace("plugins {", "// Forçando sincronização do gradle-wrapper\nplugins {")

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
