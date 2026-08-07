with open("app/src/main/java/com/example/data/FirebaseService.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i == 175 and "            }" in line:
        new_lines.append(line)
        new_lines.append("""            else {
                lastError = "Chaves do Firebase não encontradas ou inválidas.\\n" +
                            "API_KEY: ${if (rawApiKey == \\"dummy\\") \\"Ausente\\" else \\"OK\\"}\\n" +
                            "PROJECT_ID: ${if (rawProjectId == \\"dummy\\") \\"Ausente\\" else \\"OK\\"}\\n" +
                            "APP_ID: ${if (rawAppId == \\"dummy\\") \\"Ausente\\" else \\"OK\\"}"
            }\n""")
        continue
    new_lines.append(line)

with open("app/src/main/java/com/example/data/FirebaseService.kt", "w") as f:
    f.writelines(new_lines)
