import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """                composable("mestre") {
                    MestreScreen(
                        viewModel = viewModel,
                        onNavigateToAdmin = { navController.navigate("admin") },
                        onNavigateBack = {
                            navController.popBackStack()
                        }
                    )
                }"""

replacement = """                composable("mestre") {
                    MestreScreen(
                        viewModel = viewModel,
                        onNavigateToAdmin = { navController.navigate("admin") },
                        onNavigateToManageTabs = { navController.navigate("manage_tabs") },
                        onNavigateToManageProducts = { navController.navigate("manage_products") },
                        onNavigateBack = {
                            navController.popBackStack()
                        }
                    )
                }
                composable("manage_tabs") {
                    ManageTabsScreen(viewModel = viewModel, onNavigateBack = { navController.popBackStack() })
                }
                composable("manage_products") {
                    ManageProductsScreen(viewModel = viewModel, onNavigateBack = { navController.popBackStack() })
                }"""

content = content.replace(target, replacement)

# Add the new tabs to the LoginDrawerContent
drawer_target = """        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Categorias","""

drawer_replacement = """        Spacer(modifier = Modifier.height(16.dp))
        
        val dynamicTabs by viewModel.dynamicTabs.collectAsState()
        if (dynamicTabs.isNotEmpty()) {
            Text(
                text = "Abas Adicionais",
                style = MaterialTheme.typography.titleLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.align(Alignment.Start)
            )
            Spacer(modifier = Modifier.height(8.dp))
            dynamicTabs.sortedBy { it.displayOrder }.forEach { tab ->
                TextButton(
                    onClick = {
                        scope.launch { drawerState.close() }
                        // Navigate to dynamic tab view (we will create a generic one)
                        // but wait, we need a way to pass ID.
                        // For now we will just use a generic route
                        navController.navigate("dynamic_tab/${tab.id}")
                    },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text(tab.title)
                }
            }
            Spacer(modifier = Modifier.height(16.dp))
            HorizontalDivider()
            Spacer(modifier = Modifier.height(16.dp))
        }
        
        Text(
            text = "Categorias","""

content = content.replace(drawer_target, drawer_replacement)

# Add route for dynamic tab
route_target = """                composable("search") {"""

route_replacement = """                composable("dynamic_tab/{tabId}") { backStackEntry ->
                    val tabId = backStackEntry.arguments?.getString("tabId")?.toIntOrNull()
                    val dynamicTabs by viewModel.dynamicTabs.collectAsState()
                    val tab = dynamicTabs.find { it.id == tabId }
                    if (tab != null) {
                        DynamicTabScreen(tab = tab, onNavigateBack = { navController.popBackStack() })
                    } else {
                        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                            Text("Aba não encontrada.")
                        }
                    }
                }
                composable("search") {"""

content = content.replace(route_target, route_replacement)


with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
