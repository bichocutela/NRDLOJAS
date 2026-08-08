with open('app/src/main/java/com/example/ui/SearchScreen.kt', 'r') as f:
    lines = f.readlines()

start_idx = -1
for i, line in enumerate(lines):
    if 'fun SearchScreen(' in line:
        start_idx = i
        break

if start_idx != -1:
    line_with_def = lines[start_idx]
    # find the last '{' in the line
    brace_pos = line_with_def.rfind('{')
    
    count = 1
    started = True
    
    for i in range(start_idx, len(lines)):
        start_char_idx = brace_pos + 1 if i == start_idx else 0
        for char_idx in range(start_char_idx, len(lines[i])):
            char = lines[i][char_idx]
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
                if count == 0:
                    print(f"SearchScreen block ends at line {i+1}")
                    print(f"Next line: {lines[min(i+1, len(lines)-1)].strip()}")
                    break
        if count == 0:
            break

    print(f"Remaining brace count: {count}")
