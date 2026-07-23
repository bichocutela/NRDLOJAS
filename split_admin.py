import re

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

target = """fun AdminScreen(viewModel: MainViewModel, onNavigateBack: () -> Unit) {"""
replacement = """fun AdminScreen(viewModel: MainViewModel, onNavigateBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Administração") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Voltar"
                        )
                    }
                }
            )
        }
    ) { innerPadding ->
        Box(modifier = Modifier.padding(innerPadding)) {
            AdminScreenContent(viewModel = viewModel)
        }
    }
}

@Composable
fun AdminScreenContent(viewModel: MainViewModel) {"""

# Also need to remove the Scaffold from the old AdminScreen code, which is tricky with regex.
# Let's just write a more robust parser or just use sed/awk.
