import sys

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

target = """    val runNumber = System.getenv("GITHUB_RUN_NUMBER")?.toIntOrNull() ?: 1
    versionCode = 59
    versionName = "1.0.59\""""

replacement = """    versionCode = System.getenv("APP_VERSION_CODE")?.toIntOrNull() ?: 59
    versionName = System.getenv("APP_VERSION_NAME") ?: "1.0.59\""""

if target in content:
    content = content.replace(target, replacement)
    with open("app/build.gradle.kts", "w") as f:
        f.write(content)
    print("Patched app/build.gradle.kts successfully.")
else:
    print("Target not found in app/build.gradle.kts.")
