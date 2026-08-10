import re

file_path = "app/src/main/java/com/example/ui/SearchScreen.kt"

with open(file_path, "r") as f:
    content = f.read()

target = """@Composable
fun ThemeBanner(appTheme: String) {
    val context = LocalContext.current

    val normalizedTheme = when (appTheme.trim().lowercase()) {
        "gold" -> "gold"
        "green" -> "green"
        "blue" -> "blue"
        "orange" -> "orange"
        else -> "red"
    }

    val assetName = "themes/theme_${normalizedTheme}.jpg"
    val fallbackAssetName = "themes/theme_red.jpg"

    val bitmap = remember(normalizedTheme) {
        var b = runCatching {
            context.assets.open(assetName).use { input ->
                android.graphics.BitmapFactory.decodeStream(input)
            }
        }.getOrNull()
        
        if (b == null) {
            b = runCatching {
                context.assets.open(fallbackAssetName).use { input ->
                    android.graphics.BitmapFactory.decodeStream(input)
                }
            }.getOrNull()
        }
        b
    }

    if (bitmap != null) {
        Image(
            bitmap = bitmap.asImageBitmap(),
            contentDescription = "Banner do tema $normalizedTheme",
            modifier = Modifier
                .fillMaxSize(),
            contentScale = ContentScale.FillWidth
        )
    } else {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(MaterialTheme.colorScheme.primaryContainer)
        )
    }
}"""

replacement = """@Composable
fun ThemeBanner(appTheme: String) {
    val normalizedTheme = when (appTheme.trim().lowercase()) {
        "gold" -> "gold"
        "green" -> "green"
        "blue" -> "blue"
        "orange" -> "orange"
        else -> "red"
    }

    val imageUrl = "https://kkayksyzksexoarpfxyj.supabase.co/storage/v1/object/public/nrdlojas-images/themes/theme_${normalizedTheme}.jpg"

    AsyncImage(
        model = imageUrl,
        contentDescription = "Banner do tema $normalizedTheme",
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.primaryContainer),
        contentScale = ContentScale.FillWidth
    )
}"""

if target in content:
    with open(file_path, "w") as f:
        f.write(content.replace(target, replacement))
    print("Patched successfully")
else:
    print("Target not found. Looking closely...")
    # Just to be sure, let's use regex
    match = re.search(r"@Composable\s+fun ThemeBanner.*?^}", content, re.MULTILINE | re.DOTALL)
    if match:
        with open(file_path, "w") as f:
            f.write(content[:match.start()] + replacement + content[match.end():])
        print("Patched successfully via regex")
    else:
        print("Could not patch!")
