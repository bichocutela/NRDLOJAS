import sys

with open("app/src/main/java/com/example/ui/AboutScreen.kt", "r") as f:
    content = f.read()

target = """                            val currentVersion = try {
                                context.packageManager.getPackageInfo(context.packageName, 0).versionName
                            } catch (e: Exception) {
                                "1.0"
                            }
                            // Simplified version check
                            if (tag.removePrefix("v") != currentVersion) {"""

replacement = """                            val currentVersion = com.example.BuildConfig.VERSION_NAME
                            
                            // Numeric version check
                            val remoteTag = tag.removePrefix("v")
                            val currentParts = currentVersion.split(".").map { it.toIntOrNull() ?: 0 }
                            val remoteParts = remoteTag.split(".").map { it.toIntOrNull() ?: 0 }
                            
                            var isNewer = false
                            val maxLength = maxOf(currentParts.size, remoteParts.size)
                            for (i in 0 until maxLength) {
                                val c = currentParts.getOrElse(i) { 0 }
                                val r = remoteParts.getOrElse(i) { 0 }
                                if (r > c) {
                                    isNewer = true
                                    break
                                } else if (r < c) {
                                    break
                                }
                            }
                            
                            if (isNewer) {"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/AboutScreen.kt", "w") as f:
        f.write(content)
    print("Patched AboutScreen 2 successfully.")
else:
    print("Target not found in AboutScreen 2.")
