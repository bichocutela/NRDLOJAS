import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

imports = """import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.Color
import android.os.Vibrator
import android.content.Context
import android.os.VibrationEffect
import android.os.Build
"""
if "import android.os.Vibrator" not in content:
    content = content.replace("import androidx.compose.ui.text.font.FontWeight", imports)

# Make SearchScreen grab preferences
search_screen_old = """fun SearchScreen(viewModel: MainViewModel, onOpenDrawer: () -> Unit) {
    val searchQuery by viewModel.searchQuery.collectAsState()"""

search_screen_new = """fun SearchScreen(viewModel: MainViewModel, onOpenDrawer: () -> Unit) {
    val searchQuery by viewModel.searchQuery.collectAsState()
    val vibrateOnClick by viewModel.userPreferences.vibrateOnClick.collectAsState(initial = true)
    val vibrateOnFound by viewModel.userPreferences.vibrateOnFound.collectAsState(initial = true)
    val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)
    val boldOutline by viewModel.userPreferences.boldOutline.collectAsState(initial = false)
    val uppercaseBold by viewModel.userPreferences.uppercaseBold.collectAsState(initial = false)
    val context = LocalContext.current
    
    val vibrator = remember { context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator }
    
    fun triggerVibration() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            vibrator.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))
        } else {
            @Suppress("DEPRECATION")
            vibrator.vibrate(50)
        }
    }
"""

if "val vibrateOnClick" not in content:
    content = content.replace(search_screen_old, search_screen_new)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
