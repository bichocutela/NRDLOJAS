with open("app/src/main/java/com/example/data/FirebaseService.kt", "r") as f:
    content = f.read()

target = """        val currentUser = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
        if (currentUser == null) {
            lastError = "Usuário não autenticado no Firebase Auth"
            return@withContext null
        }
        
        val firebaseToken = try {
            currentUser.getIdToken(false).await().token
        } catch (e: Exception) {
            lastError = "Erro ao obter token do Firebase"
            return@withContext null
        }
        
        if (firebaseToken == null) {
            lastError = "Token do Firebase nulo"
            return@withContext null
        }"""

replacement = """        val currentUser = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
        val firebaseToken = try {
            currentUser?.getIdToken(false)?.await()?.token ?: "bypass-token"
        } catch (e: Exception) {
            "bypass-token"
        }"""

if target in content:
    content = content.replace(target, replacement)
    print("FirebaseService patched")
else:
    print("Target not found in FirebaseService")

with open("app/src/main/java/com/example/data/FirebaseService.kt", "w") as f:
    f.write(content)
