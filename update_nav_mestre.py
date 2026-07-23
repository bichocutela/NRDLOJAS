import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """                composable("mestre") {
                    MestreScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }"""

replacement = """                composable("mestre") {
                    MestreScreen(
                        viewModel = viewModel,
                        onNavigateToAdmin = { navController.navigate("admin") },
                        onNavigateBack = {
                            navController.popBackStack()
                        }
                    )
                }"""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
