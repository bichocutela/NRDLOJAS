with open("app/src/main/java/com/example/data/AuthRepository.kt", "r") as f:
    content = f.read()

target = """        } catch (e: kotlinx.coroutines.TimeoutCancellationException) {
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
        } finally {"""

replacement = """        } catch (e: kotlinx.coroutines.TimeoutCancellationException) {
            android.util.Log.e("LoginDebug", "Erro: Timeout no login (demorou muito)", e)
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("O Firebase demorou demais para responder.")
        } catch (e: com.google.firebase.FirebaseNetworkException) {
            android.util.Log.e("LoginDebug", "Erro de rede real (FirebaseNetworkException): ${e.message}", e)
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("sem internet")
        } catch (e: com.google.firebase.auth.FirebaseAuthInvalidCredentialsException) {
            android.util.Log.e("LoginDebug", "Erro credentials (FirebaseAuthInvalidCredentialsException): ${e.message}", e)
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("senha incorreta")
        } catch (e: com.google.firebase.auth.FirebaseAuthInvalidUserException) {
            android.util.Log.e("LoginDebug", "Erro user (FirebaseAuthInvalidUserException): ${e.message}", e)
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("usuário inexistente")
        } catch (e: com.google.firebase.FirebaseTooManyRequestsException) {
            android.util.Log.e("LoginDebug", "Muitas tentativas (FirebaseTooManyRequestsException): ${e.message}", e)
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error("muitas tentativas, tente novamente mais tarde")
        } catch (e: com.google.firebase.FirebaseException) {
            android.util.Log.e("LoginDebug", "Erro do Firebase (FirebaseException): ${e.message}", e)
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error(e.message ?: "Erro no Firebase")
        } catch (e: Exception) {
            android.util.Log.e("LoginDebug", "Erro geral/desconhecido: ${e.javaClass.simpleName} - ${e.message}", e)
            val msg = e.message?.lowercase() ?: ""
            val erroMsg = when {
                msg.contains("password") || msg.contains("credential") -> "senha incorreta"
                msg.contains("no user") || msg.contains("not found") -> "usuário inexistente"
                msg.contains("network") || msg.contains("host") -> "sem internet"
                msg.contains("format") || msg.contains("badly") -> "formato de usuário inválido"
                else -> "erro técnico: ${e.message}"
            }
            _authState.value = AuthState.Unauthenticated
            AuthResult.Error(erroMsg)
        } finally {"""

if target in content:
    with open("app/src/main/java/com/example/data/AuthRepository.kt", "w") as f:
        f.write(content.replace(target, replacement))
    print("AuthRepository.kt patched.")
else:
    print("Target not found in AuthRepository.kt")
