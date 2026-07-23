import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Update NavHost
navhost_target = """                composable("settings") {
                    SettingsScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }
            }
        }
    }
}"""

navhost_replacement = """                composable("settings") {
                    SettingsScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }
                composable("about") {
                    AboutScreen(onNavigateBack = {
                        navController.popBackStack()
                    })
                }
            }
        }
    }
}"""

content = content.replace(navhost_target, navhost_replacement)


drawer_target = """    onGoToAdmin: () -> Unit,
    onGoToSettings: () -> Unit
) {"""

drawer_replacement = """    onGoToAdmin: () -> Unit,
    onGoToSettings: () -> Unit,
    onGoToAbout: () -> Unit
) {"""

content = content.replace(drawer_target, drawer_replacement)

# Update LoginDrawerContent call in drawerContent block
drawer_content_target = """                        onGoToSettings = {
                            scope.launch { drawerState.close() }
                            navController.navigate("settings")
                        }"""

drawer_content_replacement = """                        onGoToSettings = {
                            scope.launch { drawerState.close() }
                            navController.navigate("settings")
                        },
                        onGoToAbout = {
                            scope.launch { drawerState.close() }
                            navController.navigate("about")
                        }"""

content = content.replace(drawer_content_target, drawer_content_replacement)

# Add "Sobre" button below "Configurações"
drawer_button_target = """        Button(
            onClick = onGoToSettings,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Configurações")
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        HorizontalDivider()"""

drawer_button_replacement = """        Button(
            onClick = onGoToSettings,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Configurações")
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = onGoToAbout,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Sobre")
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        HorizontalDivider()"""

content = content.replace(drawer_button_target, drawer_button_replacement)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
