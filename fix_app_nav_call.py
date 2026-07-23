import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """                    onLogout = {
                        sharedPref.edit().putBoolean("is_logged_in", false).apply()
                        isLoggedIn = false
                        scope.launch { drawerState.close() }
                    },
                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    },
                    onGoToSettings = {
                        scope.launch { drawerState.close() }
                        navController.navigate("settings")
                    }
                )"""

replacement = """                    onLogout = {
                        sharedPref.edit().putBoolean("is_logged_in", false).apply()
                        isLoggedIn = false
                        scope.launch { drawerState.close() }
                    },
                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    },
                    onGoToSettings = {
                        scope.launch { drawerState.close() }
                        navController.navigate("settings")
                    },
                    onGoToAbout = {
                        scope.launch { drawerState.close() }
                        navController.navigate("about")
                    }
                )"""

if target in content:
    content = content.replace(target, replacement)
else:
    print("TARGET NOT FOUND")

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
