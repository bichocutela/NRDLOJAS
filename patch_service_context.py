import re

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    content = f.read()

content = content.replace('var lastError: String? = null', 'var lastError: String? = null\n    private var appContext: android.content.Context? = null')
content = content.replace('fun initialize(context: android.content.Context) {\n        // Inicialização removida conforme solicitado (não usar signInAnonymously).\n    }', 'fun initialize(context: android.content.Context) {\n        appContext = context.applicationContext\n    }')

# Remove context from uploadImageToStorage and uploadBanner parameters
content = content.replace('suspend fun uploadImageToStorage(context: android.content.Context, uri: android.net.Uri, path: String): String?', 'suspend fun uploadImageToStorage(uri: android.net.Uri, path: String): String?')
content = content.replace('suspend fun uploadBanner(context: android.content.Context, uri: android.net.Uri): String?', 'suspend fun uploadBanner(uri: android.net.Uri): String?')
content = content.replace('val contentResolver = context.contentResolver', 'val ctx = appContext ?: return@withContext null\n            val contentResolver = ctx.contentResolver')
content = content.replace('val mimeType = getMimeType(context, uri)', 'val mimeType = getMimeType(ctx, uri)')
content = content.replace('val extension = MimeTypeMap.getSingleton().getExtensionFromMimeType(getMimeType(context, uri)) ?: "jpg"', 'val ctx = appContext ?: return null\n            val extension = MimeTypeMap.getSingleton().getExtensionFromMimeType(getMimeType(ctx, uri)) ?: "jpg"')
content = content.replace('val downloadUrl = uploadImageToStorage(context, uri, path)', 'val downloadUrl = uploadImageToStorage(uri, path)')

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
    f.write(content)
print("Patched context in FirebaseService")
