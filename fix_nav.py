import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Add composable settings
nav_host_end = """                composable("admin") {
                    AdminScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }"""

nav_host_new = """                composable("admin") {
                    AdminScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }
                composable("settings") {
                    SettingsScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }"""

if "composable(\"settings\")" not in content:
    content = content.replace(nav_host_end, nav_host_new)

# Add Settings button to drawer
drawer_end = """        } else {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Administrador",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = onGoToAdmin,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Acessar Painel Administrativo")
            }
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedButton(
                onClick = onLogout,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Sair")
            }
        }
        
        if (loginStatus != null) {"""

drawer_new = """        } else {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Administrador",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = onGoToAdmin,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Acessar Painel Administrativo")
            }
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedButton(
                onClick = onLogout,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Sair")
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        Button(
            onClick = { onGoToAdmin() /* we will replace this with onGoToSettings */ },
            modifier = Modifier.fillMaxWidth(),
            colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
        ) {
            Text("Configurações")
        }
        
        if (loginStatus != null) {"""

# Need a better way to add the config button
# Let's change the parameters of LoginDrawerContent to take onGoToSettings
old_drawer_def = """@Composable
fun LoginDrawerContent(
    viewModel: MainViewModel,
    isLoggedIn: Boolean,
    onLoginSuccess: () -> Unit,
    onLogout: () -> Unit,
    onGoToAdmin: () -> Unit
) {"""

new_drawer_def = """@Composable
fun LoginDrawerContent(
    viewModel: MainViewModel,
    isLoggedIn: Boolean,
    onLoginSuccess: () -> Unit,
    onLogout: () -> Unit,
    onGoToAdmin: () -> Unit,
    onGoToSettings: () -> Unit
) {"""

content = content.replace(old_drawer_def, new_drawer_def)
content = content.replace("LoginDrawerContent(\n                                viewModel = viewModel,", "LoginDrawerContent(\n                                viewModel = viewModel,\n                                onGoToSettings = {\n                                    scope.launch { drawerState.close() }\n                                    navController.navigate(\"settings\")\n                                },")

content = content.replace("LoginDrawerContent(\n                                    viewModel = viewModel,", "LoginDrawerContent(\n                                    viewModel = viewModel,\n                                    onGoToSettings = {\n                                        scope.launch { drawerState.close() }\n                                        navController.navigate(\"settings\")\n                                    },")

# Add the button itself
btn_insert_target = """                if (loginStatus != null) {
            Spacer(modifier = Modifier.height(16.dp))"""
btn_insert_new = """        Spacer(modifier = Modifier.height(24.dp))
        OutlinedButton(
            onClick = onGoToSettings,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Configurações")
        }
        
        if (loginStatus != null) {
            Spacer(modifier = Modifier.height(16.dp))"""
if "onClick = onGoToSettings," not in content:
    content = content.replace(btn_insert_target, btn_insert_new)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
