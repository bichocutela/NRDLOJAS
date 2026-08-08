with open("app/src/main/java/com/example/data/AuthRepository.kt", "r") as f:
    content = f.read()

target = """    suspend fun login(email: String, pass: String): AuthResult {
        if (!isConfigured) return AuthResult.Error("Firebase não configurado. Adicione o google-services.json.")
        
        return try {
            _authState.value = AuthState.Loading
            val auth = FirebaseAuth.getInstance()
            val result = auth.signInWithEmailAndPassword(email, pass).await()
            _authState.value = AuthState.Authenticated(result.user?.email ?: "")
            AuthResult.Success(result.user?.email ?: "")
        } catch (e: Exception) {
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error(e.message ?: "Erro desconhecido ao fazer login")
        }
    }"""

replacement = """    suspend fun login(email: String, pass: String): AuthResult {
        if (!isConfigured) return AuthResult.Error("Firebase indisponível (não configurado).")
        
        return try {
            _authState.value = AuthState.Loading
            android.util.Log.d("LoginDebug", "Iniciando Firebase login para: $email")
            val auth = FirebaseAuth.getInstance()
            val result = kotlinx.coroutines.withTimeout(15000L) {
                auth.signInWithEmailAndPassword(email, pass).await()
            }
            val authenticatedEmail = result.user?.email ?: ""
            android.util.Log.d("LoginDebug", "Firebase login sucesso. currentUser email: $authenticatedEmail")
            _authState.value = AuthState.Authenticated(authenticatedEmail)
            AuthResult.Success(authenticatedEmail)
        } catch (e: kotlinx.coroutines.TimeoutCancellationException) {
            android.util.Log.e("LoginDebug", "Erro: Timeout no login (sem internet?)")
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("sem internet")
        } catch (e: com.google.firebase.auth.FirebaseAuthInvalidCredentialsException) {
            android.util.Log.e("LoginDebug", "Erro credentials: ${e.message}")
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("senha incorreta")
        } catch (e: com.google.firebase.auth.FirebaseAuthInvalidUserException) {
            android.util.Log.e("LoginDebug", "Erro user: ${e.message}")
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("usuário inexistente")
        } catch (e: Exception) {
            android.util.Log.e("LoginDebug", "Erro geral: ${e.message}")
            val msg = e.message?.lowercase() ?: ""
            val erroMsg = when {
                msg.contains("password") || msg.contains("credential") -> "senha incorreta"
                msg.contains("no user") || msg.contains("not found") -> "usuário inexistente"
                msg.contains("network") || msg.contains("host") -> "sem internet"
                msg.contains("format") || msg.contains("badly") -> "formato de usuário inválido"
                else -> "erro ao fazer login: ${e.message}"
            }
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error(erroMsg)
        } finally {
            if (_authState.value == AuthState.Loading) {
                 _authState.value = AuthState.Unauthenticated
            }
        }
    }"""

if target in content:
    with open("app/src/main/java/com/example/data/AuthRepository.kt", "w") as f:
        f.write(content.replace(target, replacement))
    print("AuthRepository.kt patched.")
else:
    print("Target not found in AuthRepository.kt")
