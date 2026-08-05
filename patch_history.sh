sed -i '787,863d' app/src/main/java/com/example/ui/SearchScreen.kt
sed -i '786a \
    if (showDialog) {\
        ProductBarcodeDialog(product = product, onDismiss = { showDialog = false })\
    }' app/src/main/java/com/example/ui/SearchScreen.kt
