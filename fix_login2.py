import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Update the drawer UI for Mestre
admin_panel_btn_target = """            if (userRole == "mestre") {
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

admin_panel_btn_replacement = """            Button(
                onClick = onGoToAdmin,
                modifier = Modifier.fillMaxWidth()
            ) {
                if (userRole == "mestre") {
                    Text("Acessar Painel Mestre")
                } else {
                    Text("Acessar Painel Administrativo")
                }
            }"""

content = content.replace(admin_panel_btn_target, admin_panel_btn_replacement)


# Also in the route setup:
route_target = """                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    },"""

route_replacement = """                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        if (userRole == "mestre") {
                            navController.navigate("mestre")
                        } else {
                            navController.navigate("admin")
                        }
                    },"""

content = content.replace(route_target, route_replacement)


# Add the mestre composable
navhost_target = """                composable("admin") {
                    AdminScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }"""

navhost_replacement = """                composable("admin") {
                    AdminScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }
                composable("mestre") {
                    MestreScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }"""

content = content.replace(navhost_target, navhost_replacement)

# Let's fix the loginStatus text
login_status_target = """color = if (loginStatus == "Login com sucesso!") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error"""
login_status_replacement = """color = if (loginStatus?.startsWith("Login") == true) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error"""

content = content.replace(login_status_target, login_status_replacement)


with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
