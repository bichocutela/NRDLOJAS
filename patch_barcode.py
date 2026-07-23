import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Add imports
imports_to_add = """import android.graphics.Bitmap
import com.google.zxing.BarcodeFormat
import com.google.zxing.MultiFormatWriter
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.foundation.Image
import androidx.compose.ui.graphics.ImageBitmap
import androidx.compose.ui.layout.ContentScale
"""
if "import com.google.zxing.BarcodeFormat" not in content:
    content = content.replace("import com.example.data.Product", "import com.example.data.Product\n" + imports_to_add)

history_old = """            text = {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = product.code,
                        style = MaterialTheme.typography.displayMedium.copy(fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.primary)
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "Código de barras / Referência",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            },"""

history_new = """            text = {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
                    Text(
                        text = product.code,
                        style = MaterialTheme.typography.displayMedium.copy(fontWeight = FontWeight.Black, color = MaterialTheme.colorScheme.primary)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    val barcodeBitmap = generateBarcodeBitmap(product.code)
                    if (barcodeBitmap != null) {
                        Image(
                            bitmap = barcodeBitmap,
                            contentDescription = "Código de barras",
                            contentScale = ContentScale.FillBounds,
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(80.dp)
                                .padding(horizontal = 16.dp)
                        )
                        Spacer(modifier = Modifier.height(16.dp))
                    }
                    
                    Text(
                        text = "Código de barras / Referência",
                        style = MaterialTheme.typography.bodyMedium
                    )
                }
            },"""

if "generateBarcodeBitmap(product.code)" not in content:
    content = content.replace(history_old, history_new)

# Add generateBarcodeBitmap function
if "fun generateBarcodeBitmap" not in content:
    content += """
fun generateBarcodeBitmap(data: String): ImageBitmap? {
    try {
        val writer = MultiFormatWriter()
        val bitMatrix = writer.encode(data, BarcodeFormat.CODE_128, 600, 200)
        val width = bitMatrix.width
        val height = bitMatrix.height
        val bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888)
        for (x in 0 until width) {
            for (y in 0 until height) {
                bitmap.setPixel(x, y, if (bitMatrix.get(x, y)) android.graphics.Color.BLACK else android.graphics.Color.WHITE)
            }
        }
        return bitmap.asImageBitmap()
    } catch (e: Exception) {
        return null
    }
}
"""

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
