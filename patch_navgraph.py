with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target1 = """    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var loginStatus by remember { mutableStateOf<String?>(null) }
    val categories by viewModel.productsCountByCategory.collectAsState()"""

replacement1 = """    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var loginStatus by remember { mutableStateOf<String?>(null) }
    var isLoading by remember { mutableStateOf(false) }
    val categories by viewModel.productsCountByCategory.collectAsState()"""

target2 = """            Button(
                onClick = {
                    val email = if (username == "mestre") "mestre@nrdlojas.com"
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
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Entrar")
            }"""

replacement2 = """            Button(
                onClick = {
                    if (isLoading) return@Button
                    val inputUser = username.trim()
                    android.util.Log.d("LoginDebug", "Botão Entrar clicado. Usuário recebido: $inputUser")
                    val email = if (inputUser == "mestre") "mestre@nrdlojas.com"
                        else if (inputUser == "admin") "admin@nrdlojas.com"
                        else if (!inputUser.contains("@")) "${inputUser}@nrdlojas.com" 
                        else inputUser
                    android.util.Log.d("LoginDebug", "E-mail normalizado: $email")
                    
                    scope.launch {
                        isLoading = true
                        loginStatus = "Autenticando..."
                        try {
                            val result = viewModel.authRepository.login(email, password)
                            if (result is com.example.data.AuthResult.Success) {
                                loginStatus = null
                                val role = if (result.email == "mestre@nrdlojas.com") "mestre"
                                           else if (result.email == "admin@nrdlojas.com") "admin"
                                           else "usuario"
                                android.util.Log.d("LoginDebug", "Login sucesso na UI. Role: $role. Navegando...")
                                onLoginSuccess(role)
                            } else if (result is com.example.data.AuthResult.Error) {
                                android.util.Log.e("LoginDebug", "Falha no login: ${result.message}")
                                loginStatus = result.message
                            }
                        } catch (e: Exception) {
                            android.util.Log.e("LoginDebug", "Exceção não tratada na UI: ${e.message}")
                            loginStatus = "Erro inesperado: ${e.message}"
                        } finally {
                            isLoading = false
                        }
                    }
                },
                enabled = !isLoading,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text(if (isLoading) "Autenticando..." else "Entrar")
            }"""

if target1 in content and target2 in content:
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
        f.write(content)
    print("AppNavGraph.kt patched.")
else:
    print("Targets not found in AppNavGraph.kt")
