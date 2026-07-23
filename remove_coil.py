import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

coil_init = """        // Configure explicit image caching for faster loading and offline support
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

content = content.replace(coil_init, "")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
