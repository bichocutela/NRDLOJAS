import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """        Scaffold(
            bottomBar = {
                NavigationBar {
                    val navBackStackEntry by navController.currentBackStackEntryAsState()
                    val currentDestination = navBackStackEntry?.destination

                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Search, contentDescription = "Pesquisa") },
                        label = { Text("Pesquisa") },
                        selected = currentDestination?.hierarchy?.any { it.route == "search" } == true,
                        onClick = {
                            navController.navigate("search") {
                                popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.AutoAwesome, contentDescription = "Assistente") },
                        label = { Text("Assistente IA") },
                        selected = currentDestination?.hierarchy?.any { it.route == "assistant" } == true,
                        onClick = {
                            navController.navigate("assistant") {
                                popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                                launchSingleTop = true
                                restoreState = true
                            }
                        }
                    )
                }
            }
        ) { innerPadding ->"""

replacement = """        Scaffold(
        ) { innerPadding ->"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)

