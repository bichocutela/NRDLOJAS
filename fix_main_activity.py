import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports_to_add = """import coil.Coil
import coil.ImageLoader
import coil.disk.DiskCache
import coil.memory.MemoryCache
"""

if "coil.Coil" not in content:
    content = content.replace("import android.os.Bundle", imports_to_add + "import android.os.Bundle")

setup_code = """    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Configure explicit image caching for faster loading and offline support
        val imageLoader = ImageLoader.Builder(this)
            .memoryCache {
                MemoryCache.Builder(this)
                    .maxSizePercent(0.25)
                    .build()
            }
            .diskCache {
                DiskCache.Builder()
                    .directory(this.cacheDir.resolve("image_cache"))
                    .maxSizePercent(0.05) // Use 5% of device free space for images
                    .build()
            }
            .crossfade(true)
            .build()
        Coil.setImageLoader(imageLoader)"""

content = content.replace("    override fun onCreate(savedInstanceState: Bundle?) {\n        super.onCreate(savedInstanceState)", setup_code)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
