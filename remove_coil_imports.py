with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

content = content.replace("import coil.Coil\n", "")
content = content.replace("import coil.ImageLoader\n", "")
content = content.replace("import coil.disk.DiskCache\n", "")
content = content.replace("import coil.memory.MemoryCache\n", "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
