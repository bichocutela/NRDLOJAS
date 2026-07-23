import os

with open(".github/workflows/main.yml", "r") as f:
    content = f.read()

replacement = """    - name: Fix Corrupt Gradle Wrapper Jar
      run: |
        rm -f gradle/wrapper/gradle-wrapper.jar
        curl -fsSL -o gradle/wrapper/gradle-wrapper.jar "https://raw.githubusercontent.com/gradle/gradle/v9.3.1/gradle/wrapper/gradle-wrapper.jar"

    - name: Grant execute permission for gradlew
"""

content = content.replace("    - name: Grant execute permission for gradlew\n", replacement)

with open(".github/workflows/main.yml", "w") as f:
    f.write(content)
