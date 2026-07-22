import re

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

# Add ArrowBack icon import
imports = """import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.ArrowBack
"""
content = content.replace("import androidx.compose.material.icons.filled.AddAPhoto", imports + "import androidx.compose.material.icons.filled.AddAPhoto")

content = content.replace("fun AdminScreen(viewModel: MainViewModel) {", "fun AdminScreen(viewModel: MainViewModel, onNavigateBack: () -> Unit) {")

top_app_bar_old = """        topBar = {
            TopAppBar(
                title = { Text("Painel Administrativo") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        },"""

top_app_bar_new = """        topBar = {
            TopAppBar(
                title = { Text("Painel Administrativo") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Voltar",
                            tint = MaterialTheme.colorScheme.onPrimary
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primary,
                    titleContentColor = MaterialTheme.colorScheme.onPrimary
                )
            )
        },"""

content = content.replace(top_app_bar_old, top_app_bar_new)

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "w") as f:
    f.write(content)

