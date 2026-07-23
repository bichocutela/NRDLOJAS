import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Update SharedPreferences logic in AppNavGraph
shared_prefs_target = """    val sharedPref = remember { context.getSharedPreferences("admin_prefs", Context.MODE_PRIVATE) }
    var isLoggedIn by remember { mutableStateOf(sharedPref.getBoolean("is_logged_in", false)) }"""

shared_prefs_replacement = """    val sharedPref = remember { context.getSharedPreferences("admin_prefs", Context.MODE_PRIVATE) }
    var isLoggedIn by remember { mutableStateOf(sharedPref.getBoolean("is_logged_in", false)) }
    var userRole by remember { mutableStateOf(sharedPref.getString("user_role", "admin") ?: "admin") }"""

content = content.replace(shared_prefs_target, shared_prefs_replacement)

# Update LoginDrawerContent parameters
drawer_target = """fun LoginDrawerContent(
    viewModel: MainViewModel,
    isLoggedIn: Boolean,
    onLoginSuccess: () -> Unit,"""

drawer_replacement = """fun LoginDrawerContent(
    viewModel: MainViewModel,
    isLoggedIn: Boolean,
    userRole: String,
    onLoginSuccess: (String) -> Unit,"""

content = content.replace(drawer_target, drawer_replacement)

# Update LoginDrawerContent call
call_target = """                LoginDrawerContent(
                    viewModel = viewModel,
                    isLoggedIn = isLoggedIn,
                    onLoginSuccess = {"""

call_replacement = """                LoginDrawerContent(
                    viewModel = viewModel,
                    isLoggedIn = isLoggedIn,
                    userRole = userRole,
                    onLoginSuccess = { role ->
                        sharedPref.edit()
                            .putBoolean("is_logged_in", true)
                            .putString("user_role", role)
                            .apply()
                        isLoggedIn = true
                        userRole = role
                        scope.launch { drawerState.close() }"""

content = content.replace(call_target, call_replacement)

# Remove the hardcoded onLoginSuccess() which lacked args in old code
call_target2 = """                        sharedPref.edit().putBoolean("is_logged_in", true).apply()
                        isLoggedIn = true
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    },
                    onLogout = {"""

call_replacement2 = """                        if (role == "mestre") {
                            navController.navigate("mestre")
                        } else {
                            navController.navigate("admin")
                        }
                    },
                    onLogout = {"""

content = content.replace(call_target2, call_replacement2)


# Update the login button logic
btn_target = """            Button(
                onClick = {
                    if (username == "admin" && password == "nrdlojas") {
                        loginStatus = "Login com sucesso!"
                        onLoginSuccess()
                    } else {
                        loginStatus = "Usuário ou senha incorretos."
                    }
                },"""

btn_replacement = """            Button(
                onClick = {
                    if (username == "mestre" && password == "nrdlojas") {
                        loginStatus = "Login Mestre realizado!"
                        onLoginSuccess("mestre")
                    } else if (username == "admin" && password == "nrdlojas") {
                        loginStatus = "Login Admin realizado!"
                        onLoginSuccess("admin")
                    } else {
                        loginStatus = "Usuário ou senha incorretos."
                    }
                },"""

content = content.replace(btn_target, btn_replacement)

# Update the drawer UI for Mestre
admin_panel_btn_target = """            Button(
                onClick = onGoToAdmin,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Acessar Painel Administrativo")
            }"""

admin_panel_btn_replacement = """            if (userRole == "mestre") {
                Button(
                    onClick = { /* Go to mestre */ },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Acessar Painel Mestre")
                }
            } else {
                Button(
                    onClick = onGoToAdmin,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Acessar Painel Administrativo")
                }
            }"""

content = content.replace(admin_panel_btn_target, admin_panel_btn_replacement)


with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
