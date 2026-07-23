import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

state_code = """
    var isScannerOpen by remember { mutableStateOf(false) }

    if (isScannerOpen) {
        BarcodeScannerScreen(
            onBarcodeScanned = { code ->
                viewModel.updateSearchQuery(code)
                isScannerOpen = false
            },
            onClose = { isScannerOpen = false }
        )
        return // Return early so we don't show the rest of the screen
    }
"""

content = content.replace("    val newProductsCount by viewModel.newProductsCount.collectAsStateWithLifecycle()", "    val newProductsCount by viewModel.newProductsCount.collectAsStateWithLifecycle()\n" + state_code)

icon_btn = """
                        } else {
                            IconButton(onClick = { isScannerOpen = true }) {
                                Icon(Icons.Default.QrCodeScanner, contentDescription = "Scanner QR", tint = MaterialTheme.colorScheme.primary)
                            }
                            IconButton(onClick = { /* TODO Voice Search */ }) {"""

content = content.replace("                        } else {\n                            IconButton(onClick = { /* TODO Voice Search */ }) {", icon_btn)

if "QrCodeScanner" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Search", "import androidx.compose.material.icons.filled.Search\nimport androidx.compose.material.icons.filled.QrCodeScanner")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
