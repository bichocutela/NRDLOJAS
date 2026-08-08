with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

content = content.replace("color = Color(0xFFE31B23), // Red color", "color = MaterialTheme.colorScheme.primary,")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
print("Patched SearchScreen Color")
