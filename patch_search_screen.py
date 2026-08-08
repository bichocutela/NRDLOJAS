import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

replacement = """
    val appTheme by viewModel.userPreferences.appTheme.collectAsStateWithLifecycle(initialValue = "red")
    
    val bannerModel = remember(appTheme, bannerImageUri) {
        val supabaseUrl = com.example.BuildConfig.SUPABASE_URL
        if (appTheme != "red") {
            "$supabaseUrl/storage/v1/object/public/nrdlojas-images/banners/themes/theme_${appTheme}.jpg"
        } else {
            if (bannerImageUri != null && bannerImageUri!!.startsWith("data:image")) {
                val base64 = bannerImageUri!!.substringAfter("base64,")
                android.util.Base64.decode(base64, android.util.Base64.DEFAULT)
            } else if (bannerImageUri != null && bannerImageUri!!.isNotEmpty()) {
                bannerImageUri
            } else {
                "$supabaseUrl/storage/v1/object/public/nrdlojas-images/banners/themes/theme_red.jpg"
            }
        }
    }
"""

if "val bannerModel =" in content:
    pattern = re.compile(r'    val bannerModel = remember\(bannerImageUri\) \{[\s\S]*?    \}')
    content = pattern.sub(replacement.strip(), content)
    with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
        f.write(content)
    print("Patched SearchScreen")
else:
    print("bannerModel not found in SearchScreen")
