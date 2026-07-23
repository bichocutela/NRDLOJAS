import os

with open("gradlew", "r") as f:
    lines = f.readlines()

insert_idx = 1
for i, line in enumerate(lines):
    if not line.startswith("#"):
        insert_idx = i
        break

injection = """
# Auto-download gradle-wrapper.jar if missing
if [ ! -f "gradle/wrapper/gradle-wrapper.jar" ]; then
    echo "Downloading gradle-wrapper.jar..."
    mkdir -p gradle/wrapper
    curl -fsSL -o gradle/wrapper/gradle-wrapper.jar "https://raw.githubusercontent.com/gradle/gradle/v9.3.1/gradle/wrapper/gradle-wrapper.jar"
fi
"""

lines.insert(insert_idx, injection)

with open("gradlew", "w") as f:
    f.writelines(lines)
