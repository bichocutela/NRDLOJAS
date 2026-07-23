import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Update LoginDrawerContent parameters
target = """    onGoToSettings: () -> Unit,
    onGoToAbout: () -> Unit
) {"""

replacement = """    onGoToSettings: () -> Unit,
    onGoToAbout: () -> Unit,
    onGoToDynamicTab: (Int) -> Unit
) {"""

content = content.replace(target, replacement)

# Update LoginDrawerContent invocation
target_call = """                    onGoToAbout = {
                        scope.launch { drawerState.close() }
                        navController.navigate("about")
                    }
                )"""

replacement_call = """                    onGoToAbout = {
                        scope.launch { drawerState.close() }
                        navController.navigate("about")
                    },
                    onGoToDynamicTab = { tabId ->
                        scope.launch { drawerState.close() }
                        navController.navigate("dynamic_tab/$tabId")
                    }
                )"""

content = content.replace(target_call, replacement_call)

# Update the drawer logic to use onGoToDynamicTab
target_logic = """                    onClick = {
                        scope.launch { drawerState.close() }
                        // Navigate to dynamic tab view (we will create a generic one)
                        // but wait, we need a way to pass ID.
                        // For now we will just use a generic route
                        navController.navigate("dynamic_tab/${tab.id}")
                    },"""

replacement_logic = """                    onClick = {
                        onGoToDynamicTab(tab.id)
                    },"""

content = content.replace(target_logic, replacement_logic)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
