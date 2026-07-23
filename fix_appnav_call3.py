with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """                    onGoToAbout = { scope.launch { drawerState.close() }; navController.navigate("about") }
                )"""

replacement = """                    onGoToAbout = { scope.launch { drawerState.close() }; navController.navigate("about") },
                    onGoToDynamicTab = { tabId ->
                        scope.launch { drawerState.close() }
                        navController.navigate("dynamic_tab/$tabId")
                    }
                )"""
content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
