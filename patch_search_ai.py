import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Add dialog in SearchScreen
dialog_code = """
    val aiProductDetails by viewModel.aiProductDetails.collectAsStateWithLifecycle()
    val isAiLoading by viewModel.isAiLoading.collectAsStateWithLifecycle()

    if (isAiLoading || aiProductDetails != null) {
        AlertDialog(
            onDismissRequest = { viewModel.clearAiProductDetails() },
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(Icons.Default.AutoAwesome, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(8.dp))
                    Text("Detalhes com IA")
                }
            },
            text = {
                if (isAiLoading) {
                    Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator()
                    }
                } else {
                    Text(aiProductDetails ?: "")
                }
            },
            confirmButton = {
                TextButton(onClick = { viewModel.clearAiProductDetails() }) {
                    Text("Fechar")
                }
            }
        )
    }
"""

content = content.replace("    val filteredProducts by viewModel.filteredProducts.collectAsStateWithLifecycle()", 
"    val filteredProducts by viewModel.filteredProducts.collectAsStateWithLifecycle()\n" + dialog_code)


# Add AutoAwesome import
if "import androidx.compose.material.icons.filled.AutoAwesome" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Search", "import androidx.compose.material.icons.filled.Search\nimport androidx.compose.material.icons.filled.AutoAwesome\nimport androidx.compose.material3.AlertDialog\nimport androidx.compose.material3.TextButton\nimport androidx.compose.material3.CircularProgressIndicator")

# Add button to ProductCard
product_card_btn = """
        Spacer(modifier = Modifier.width(8.dp))
        androidx.compose.material3.IconButton(
            onClick = { viewModel.consultProductInfoAi(product) },
            modifier = Modifier.background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
        ) {
            Icon(Icons.Default.AutoAwesome, contentDescription = "IA Info", tint = MaterialTheme.colorScheme.onTertiaryContainer)
        }
    }
}
"""

content = re.sub(r'(\s*)\}\s*\}\s*\}\s*fun MiniProductCard', r'\1}\n        }\n' + product_card_btn + '\n\nfun MiniProductCard', content)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)

