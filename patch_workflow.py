import sys

with open(".github/workflows/main.yml", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "- name: Decode Release Keystore" in line:
        new_lines.append("    - name: Create google-services.json\n")
        new_lines.append("      env:\n")
        new_lines.append("        GOOGLE_SERVICES_JSON: ${{ secrets.GOOGLE_SERVICES_JSON }}\n")
        new_lines.append("      run: |\n")
        new_lines.append("        mkdir -p app\n")
        new_lines.append("        printf '%s' \"$GOOGLE_SERVICES_JSON\" > app/google-services.json\n")
        new_lines.append("        test -s app/google-services.json\n\n")
    new_lines.append(line)

with open(".github/workflows/main.yml", "w") as f:
    f.writelines(new_lines)
