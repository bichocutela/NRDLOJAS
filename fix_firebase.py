import re

with open("app/src/main/java/com/example/data/FirebaseService.kt", "r") as f:
    content = f.read()

# Let's fix the broken part
broken_part = """                    try {
                        com.google.firebase.auth.FirebaseAuth.getInstance().signInAnonymously()
                    }
            } else {
                lastError = "Chaves ausentes: API_KEY=${if (rawApiKey==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, PROJECT_ID=${if (rawProjectId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, APP_ID=${if (rawAppId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}" catch (e: Exception) {
                        Log.e("FirebaseService", "Auth error", e)
                    }
            } else {
                lastError = "Chaves ausentes: API_KEY=${if (rawApiKey==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, PROJECT_ID=${if (rawProjectId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, APP_ID=${if (rawAppId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}"
                } catch (ex: Exception) {
                    lastError = "Init error: " + ex.message
                    Log.e("FirebaseService", "Erro ao inicializar Firebase", ex)
                }
            } else {
                lastError = "Chaves ausentes: API_KEY=${if (rawApiKey==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, PROJECT_ID=${if (rawProjectId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, APP_ID=${if (rawAppId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}"
            }"""

original_part = """                    try {
                        com.google.firebase.auth.FirebaseAuth.getInstance().signInAnonymously()
                    } catch (e: Exception) {
                        Log.e("FirebaseService", "Auth error", e)
                    }
                } catch (ex: Exception) {
                    lastError = "Init error: " + ex.message
                    Log.e("FirebaseService", "Erro ao inicializar Firebase", ex)
                }
            } else {
                lastError = "Chaves ausentes: API_KEY=${if (rawApiKey==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, PROJECT_ID=${if (rawProjectId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, APP_ID=${if (rawAppId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}"
            }
        }
    }"""

content = re.sub(r'                    try \{\n                        com\.google\.firebase\.auth\.FirebaseAuth\.getInstance\(\)\.signInAnonymously\(\)\n.*?\} catch \(ex: Exception\) \{.*?\n            \} else \{.*?\n            \}', original_part, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/data/FirebaseService.kt", "w") as f:
    f.write(content)
