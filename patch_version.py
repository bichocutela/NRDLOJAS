import re

with open('app/build.gradle.kts', 'r') as f:
    content = f.read()

content = content.replace('versionName = "1.0.$runNumber"', 'versionName = "1.0.59"')
content = content.replace('versionCode = runNumber', 'versionCode = 59')

with open('app/build.gradle.kts', 'w') as f:
    f.write(content)
print("Patched app/build.gradle.kts version")
