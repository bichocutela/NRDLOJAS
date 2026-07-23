import re

# Fix AppNavGraph
with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    nav_content = f.read()

# I messed up replacing LoginDrawerContent before, I should just make sure onGoToSettings is provided.
# Let's see how many LoginDrawerContent calls there are. Only 1 around line 42.
# Let's replace the whole call.
nav_old = """                LoginDrawerContent(
                    viewModel = viewModel,
                    isLoggedIn = false,
                    onLoginSuccess = { /* Handle success */ },
                    onLogout = { /* Handle logout */ },
                    onGoToAdmin = { 
                        scope.launch { drawerState.close() }
                        navController.navigate("admin") 
                    },
                    onGoToSettings = {
                                        scope.launch { drawerState.close() }
                                        navController.navigate("settings")
                                    }
                )"""

nav_content = nav_content.replace(nav_old, "")
nav_old_2 = """                LoginDrawerContent(
                    viewModel = viewModel,
                    isLoggedIn = false,
                    onLoginSuccess = { /* Handle success */ },
                    onLogout = { /* Handle logout */ },
                    onGoToAdmin = { 
                        scope.launch { drawerState.close() }
                        navController.navigate("admin") 
                    }
                )"""
nav_new = """                LoginDrawerContent(
                    viewModel = viewModel,
                    isLoggedIn = false,
                    onLoginSuccess = { /* Handle success */ },
                    onLogout = { /* Handle logout */ },
                    onGoToAdmin = { 
                        scope.launch { drawerState.close() }
                        navController.navigate("admin") 
                    },
                    onGoToSettings = {
                        scope.launch { drawerState.close() }
                        navController.navigate("settings")
                    }
                )"""
nav_content = nav_content.replace(nav_old_2, nav_new)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(nav_content)

# Fix SearchScreen
with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    search = f.read()

# Fix color conflict
search = re.sub(r'import androidx\.compose\.ui\.graphics\.Color\n(.*)import androidx\.compose\.ui\.graphics\.Color\n', r'import androidx.compose.ui.graphics.Color\n\1', search, flags=re.DOTALL)

# Fix repeatable annotation (probably double @Composable)
search = search.replace("@Composable\n@Composable\nfun StylizedText", "@Composable\nfun StylizedText")

# Fix missing collectAsState and getValue imports
if "import androidx.compose.runtime.collectAsState" not in search:
    search = search.replace("import androidx.compose.runtime.getValue", "import androidx.compose.runtime.getValue\nimport androidx.compose.runtime.collectAsState\nimport androidx.compose.runtime.LaunchedEffect\nimport kotlinx.coroutines.flow.collectLatest\n")

# In ProductCard, HistoryItem, MiniProductCard, the `collectAsState` is used, so we need to add @Composable to them if it was missing?
# Wait, `val vibrateOnClick by viewModel.userPreferences.vibrateOnClick.collectAsState(initial = true)`
# If they are already marked @Composable, it should work. But maybe they are not marked @Composable?
# Let's check ProductCard.

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(search)

