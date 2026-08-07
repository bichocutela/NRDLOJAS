with open("app/src/main/java/com/example/data/FirebaseService.kt", "r") as f:
    content = f.read()

old_str = """                } catch (ex: Exception) {
                    lastError = "Init error: " + ex.message
                    Log.e("FirebaseService", "Erro ao inicializar Firebase", ex)
                }
            }
        }
    }"""

new_str = """                } catch (ex: Exception) {
                    lastError = "Init error: " + ex.message
                    Log.e("FirebaseService", "Erro ao inicializar Firebase", ex)
                }
            } else {
                lastError = "Chaves do Firebase não encontradas ou inválidas.\\nAPI_KEY: ${if (rawApiKey == \\"dummy\\") \\"Ausente\\" else \\"OK\\"}\\nPROJECT_ID: ${if (rawProjectId == \\"dummy\\") \\"Ausente\\" else \\"OK\\"}\\nAPP_ID: ${if (rawAppId == \\"dummy\\") \\"Ausente\\" else \\"OK\\"}"
            }
        }
    }"""

with open("app/src/main/java/com/example/data/FirebaseService.kt", "w") as f:
    f.write(content.replace(old_str, new_str))
