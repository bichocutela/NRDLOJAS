import re

with open('app/src/main/java/com/example/ui/AppNavGraph.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'if \(username == "mestre" && password == "nrdlojas"\) \{[\s\S]*?\} else \{[\s\S]*?// Firebase Auth[\s\S]*?val email = if \(!username\.contains\("@"\)\) "\$\{username\}@nrdlojas\.com" else username[\s\S]*?scope\.launch \{[\s\S]*?loginStatus = "Autenticando\.\.\."[\s\S]*?val result = viewModel\.authRepository\.login\(email, password\)[\s\S]*?if \(result is com\.example\.data\.AuthResult\.Success\) \{[\s\S]*?loginStatus = null[\s\S]*?onLoginSuccess\(if \(username == "teste" \|\| email\.startsWith\("teste@"\)\) "teste" else "usuario"\)[\s\S]*?\} else \{[\s\S]*?// Fallback para login local se Firebase falhar \(Auth não configurado\)[\s\S]*?loginStatus = null[\s\S]*?onLoginSuccess\(if \(username == "teste" \|\| email\.startsWith\("teste@"\)\) "teste" else "usuario"\)[\s\S]*?\}[\s\S]*?\}[\s\S]*?\}')

replacement = '''val email = if (username == "mestre") "mestre@nrdlojas.com"
                        else if (username == "admin") "admin@nrdlojas.com"
                        else if (!username.contains("@")) "${username}@nrdlojas.com" 
                        else username
                    
                    scope.launch {
                        loginStatus = "Autenticando..."
                        val result = viewModel.authRepository.login(email, password)
                        if (result is com.example.data.AuthResult.Success) {
                            loginStatus = null
                            val role = if (email == "mestre@nrdlojas.com") "mestre"
                                       else if (email == "admin@nrdlojas.com") "admin"
                                       else "usuario"
                            onLoginSuccess(role)
                        } else {
                            loginStatus = "Falha no login. Verifique no Firebase."
                        }
                    }'''

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/ui/AppNavGraph.kt', 'w') as f:
    f.write(content)
print("Patched AppNavGraph login logic")
