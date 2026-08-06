sed -i 's/import androidx.compose.ui.platform.LocalLifecycleOwner/import androidx.lifecycle.compose.LocalLifecycleOwner/g' app/src/main/java/com/example/ui/BarcodeScannerScreen.kt
sed -i 's/Icons.Filled.Send/Icons.AutoMirrored.Filled.Send/g' app/src/main/java/com/example/ui/ProductBarcodeDialog.kt
