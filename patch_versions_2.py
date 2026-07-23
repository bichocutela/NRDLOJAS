import re

with open("gradle/libs.versions.toml", "r") as f:
    content = f.read()

# Revert Room versions
content = re.sub(r'roomRuntime = ".*"', 'roomRuntime = "2.7.0"', content)
content = re.sub(r'roomKtx = ".*"', 'roomKtx = "2.7.0"', content)
content = re.sub(r'roomCompiler = ".*"', 'roomCompiler = "2.7.0"', content)

# Revert CameraX versions
content = re.sub(r'cameraCamera2 = ".*"', 'cameraCamera2 = "1.5.0"', content)
content = re.sub(r'cameraLifecycle = ".*"', 'cameraLifecycle = "1.5.0"', content)
content = re.sub(r'cameraView = ".*"', 'cameraView = "1.5.0"', content)
content = re.sub(r'cameraCore = ".*"', 'cameraCore = "1.5.0"', content)

with open("gradle/libs.versions.toml", "w") as f:
    f.write(content)
