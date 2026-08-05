sed -i '681a \
    var showDialog by remember { mutableStateOf(false) }\
    if (showDialog) {\
        ProductBarcodeDialog(product = product, onDismiss = { showDialog = false })\
    }' app/src/main/java/com/example/ui/SearchScreen.kt
