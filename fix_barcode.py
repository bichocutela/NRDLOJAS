import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Add imports for FilterQuality and EncodeHintType
imports_to_add = """import androidx.compose.ui.graphics.FilterQuality
import com.google.zxing.EncodeHintType
import java.util.EnumMap
"""
content = content.replace("import com.google.zxing.BarcodeFormat", imports_to_add + "import com.google.zxing.BarcodeFormat")

# Fix Image component
old_image = """                        Image(
                            bitmap = barcodeBitmap,
                            contentDescription = "Código de barras",
                            contentScale = ContentScale.FillBounds,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(80.dp)
                                .padding(horizontal = 16.dp)
                        )"""

new_image = """                        Image(
                            bitmap = barcodeBitmap,
                            contentDescription = "Código de barras",
                            contentScale = ContentScale.FillBounds,
                            filterQuality = FilterQuality.None,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(90.dp)
                                .padding(horizontal = 24.dp)
                                .background(androidx.compose.ui.graphics.Color.White)
                        )"""
content = content.replace(old_image, new_image)

# Fix generateBarcodeBitmap
old_gen = """fun generateBarcodeBitmap(data: String): ImageBitmap? {
    try {
        val writer = MultiFormatWriter()
        val bitMatrix = writer.encode(data, BarcodeFormat.CODE_128, 600, 200)"""

new_gen = """fun generateBarcodeBitmap(data: String): ImageBitmap? {
    try {
        val writer = MultiFormatWriter()
        val hints = EnumMap<EncodeHintType, Any>(EncodeHintType::class.java)
        hints[EncodeHintType.MARGIN] = 0 // we handle margin in Compose
        
        // Generate with higher horizontal resolution to prevent artifacts, 
        // but even with FilterQuality.None, drawing sharp is best
        val bitMatrix = writer.encode(data, BarcodeFormat.CODE_128, 1024, 256, hints)"""
content = content.replace(old_gen, new_gen)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
