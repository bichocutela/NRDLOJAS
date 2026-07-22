import re

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

# Replace AppNavGraph definition
imports = """import android.content.Context
import androidx.compose.ui.platform.LocalContext
"""
content = content.replace("import androidx.compose.foundation.layout.*", imports + "import androidx.compose.foundation.layout.*")

app_nav = """@Composable
fun AppNavGraph(viewModel: MainViewModel) {
    val navController = rememberNavController()
    val drawerState = rememberDrawerState(initialValue = DrawerValue.Closed)
    val scope = rememberCoroutineScope()
    val context = LocalContext.current
    val sharedPref = remember { context.getSharedPreferences("admin_prefs", Context.MODE_PRIVATE) }
    var isLoggedIn by remember { mutableStateOf(sharedPref.getBoolean("is_logged_in", false)) }

    ModalNavigationDrawer(
        drawerState = drawerState,
        drawerContent = {
            ModalDrawerSheet {
                LoginDrawerContent(
                    viewModel = viewModel,
                    isLoggedIn = isLoggedIn,
                    onLoginSuccess = {
                        sharedPref.edit().putBoolean("is_logged_in", true).apply()
                        isLoggedIn = true
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    },
                    onLogout = {
                        sharedPref.edit().putBoolean("is_logged_in", false).apply()
                        isLoggedIn = false
                        scope.launch { drawerState.close() }
                        navController.navigate("search") {
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        }
                    },
                    onGoToAdmin = {
                        scope.launch { drawerState.close() }
                        navController.navigate("admin")
                    }
                )
            }
        }
    ) {"""
content = re.sub(r'@Composable\nfun AppNavGraph\(viewModel: MainViewModel\) \{.*?\) \{', app_nav, content, flags=re.DOTALL)

# Update AdminScreen call
admin_call = """                composable("admin") {
                    AdminScreen(viewModel, onNavigateBack = {
                        navController.popBackStack()
                    })
                }"""
content = re.sub(r'                composable\("admin"\) \{\n                    AdminScreen\(viewModel\)\n                \}', admin_call, content)

# Update LoginDrawerContent signature and body
login_content_def = """@Composable
fun LoginDrawerContent(
    viewModel: MainViewModel,
    isLoggedIn: Boolean,
    onLoginSuccess: () -> Unit,
    onLogout: () -> Unit,
    onGoToAdmin: () -> Unit
) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var loginStatus by remember { mutableStateOf<String?>(null) }
    val categories by viewModel.productsCountByCategory.collectAsState()
    var expandedCategory by remember { mutableStateOf<String?>(null) }

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
            .verticalScroll(rememberScrollState()),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        if (!isLoggedIn) {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Login",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(32.dp))
            OutlinedTextField(
                value = username,
                onValueChange = { username = it },
                label = { Text("Usuário") },
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedTextField(
                value = password,
                onValueChange = { password = it },
                label = { Text("Senha") },
                visualTransformation = PasswordVisualTransformation(),
                modifier = Modifier.fillMaxWidth()
            )
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = {
                    if (username == "admin" && password == "nrdlojas") {
                        loginStatus = "Login com sucesso!"
                        onLoginSuccess()
                    } else {
                        loginStatus = "Usuário ou senha incorretos."
                    }
                },
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Entrar")
            }
            if (loginStatus != null) {
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = loginStatus!!,
                    color = if (loginStatus == "Login com sucesso!") MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.error
                )
            }
        } else {
            Spacer(modifier = Modifier.height(24.dp))
            Text(
                text = "Administrador",
                style = MaterialTheme.typography.headlineMedium,
                color = MaterialTheme.colorScheme.primary
            )
            Spacer(modifier = Modifier.height(24.dp))
            Button(
                onClick = onGoToAdmin,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Acessar Painel Administrativo")
            }
            Spacer(modifier = Modifier.height(16.dp))
            OutlinedButton(
                onClick = onLogout,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Sair")
            }
        }
"""
content = re.sub(r'@Composable\nfun LoginDrawerContent\(viewModel: MainViewModel, onLoginSuccess: \(\) -> Unit\) \{.*?\n        \}\n', login_content_def, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)

