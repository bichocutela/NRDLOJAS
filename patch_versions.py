import re

with open("gradle/libs.versions.toml", "r") as f:
    content = f.read()

# Retrofit versions
content = re.sub(r'retrofit = ".*"', 'retrofit = "2.11.0"', content)
content = re.sub(r'converterMoshi = ".*"', 'converterMoshi = "2.11.0"', content)
content = re.sub(r'retrofitConverterSerialization = ".*"', 'retrofitConverterSerialization = "2.11.0"', content)

# Room versions
content = re.sub(r'roomRuntime = ".*"', 'roomRuntime = "2.6.1"', content)
content = re.sub(r'roomKtx = ".*"', 'roomKtx = "2.6.1"', content)
content = re.sub(r'roomCompiler = ".*"', 'roomCompiler = "2.6.1"', content)

# CameraX versions
content = re.sub(r'cameraCamera2 = ".*"', 'cameraCamera2 = "1.3.4"', content)
content = re.sub(r'cameraLifecycle = ".*"', 'cameraLifecycle = "1.3.4"', content)
content = re.sub(r'cameraView = ".*"', 'cameraView = "1.3.4"', content)
content = re.sub(r'cameraCore = ".*"', 'cameraCore = "1.3.4"', content)

with open("gradle/libs.versions.toml", "w") as f:
    f.write(content)
