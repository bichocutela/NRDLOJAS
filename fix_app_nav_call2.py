import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """                    onGoToSettings = { scope.launch { drawerState.close() }; navController.navigate("settings") },
                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    }
                )"""

replacement = """                    onGoToSettings = { scope.launch { drawerState.close() }; navController.navigate("settings") },
                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    },
                    onGoToAbout = { scope.launch { drawerState.close() }; navController.navigate("about") }
                )"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("TARGET NOT FOUND")

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
