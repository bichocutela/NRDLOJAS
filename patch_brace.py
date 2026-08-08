with open('app/src/main/java/com/example/ui/SearchScreen.kt', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    if "@Composable\nfun SectionHeader(" in "".join(lines[i:i+2]):
        # The line before this should be a brace
        if lines[i-1].strip() == "}":
            del lines[i-1]
            break

with open('app/src/main/java/com/example/ui/SearchScreen.kt', 'w') as f:
    f.writelines(lines)
