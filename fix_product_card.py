import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Helper for text modification
def inject_prefs(composable_name, content):
    pattern = r'(@Composable\nfun ' + composable_name + r'\(.*?\)\s*\{)'
    replacement = r'\1\n    val vibrateOnClick by viewModel.userPreferences.vibrateOnClick.collectAsState(initial = true)\n    val vibrateOnFound by viewModel.userPreferences.vibrateOnFound.collectAsState(initial = true)\n    val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)\n    val boldOutline by viewModel.userPreferences.boldOutline.collectAsState(initial = false)\n    val uppercaseBold by viewModel.userPreferences.uppercaseBold.collectAsState(initial = false)\n    val context = LocalContext.current\n    val vibrator = remember { context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator }\n    fun triggerVibration() {\n        if (!vibrateOnClick) return\n        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {\n            vibrator.vibrate(VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE))\n        } else {\n            @Suppress("DEPRECATION")\n            vibrator.vibrate(50)\n        }\n    }\n'
    return re.sub(pattern, replacement, content)

content = inject_prefs("ProductCard", content)
content = inject_prefs("HistoryItem", content)
content = inject_prefs("MiniProductCard", content)

# Adjust clickables to vibrate
content = content.replace(".clickable { showDialog = true }", ".clickable { triggerVibration(); showDialog = true }")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
