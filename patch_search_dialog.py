import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

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

content = content.replace("    val newProductsCount by viewModel.newProductsCount.collectAsStateWithLifecycle()", 
"    val newProductsCount by viewModel.newProductsCount.collectAsStateWithLifecycle()\n" + dialog_code)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
