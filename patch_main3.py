with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if "var updateInfo by remember" in line:
        skip = True
    if skip and "Mais tarde" in lines[i-3] and "}" in line:
        skip = False
        continue
    
    if not skip:
        new_lines.append(line)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.writelines(new_lines)
