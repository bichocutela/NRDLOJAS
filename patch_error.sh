#!/bin/bash
sed -i 's/                }/                }\n            } else {\n                lastError = "Chaves ausentes: API_KEY=${if (rawApiKey==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, PROJECT_ID=${if (rawProjectId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}, APP_ID=${if (rawAppId==\\"dummy\\") \\"FALTA\\" else \\"OK\\"}"/g' app/src/main/java/com/example/data/FirebaseService.kt
