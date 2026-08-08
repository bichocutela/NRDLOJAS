import re

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    content = f.read()

# Add OkHttp import
if 'import okhttp3' not in content:
    content = content.replace('import com.google.firebase.firestore.FirebaseFirestore', 'import com.google.firebase.firestore.FirebaseFirestore\nimport okhttp3.MediaType.Companion.toMediaType\nimport okhttp3.OkHttpClient\nimport okhttp3.Request\nimport okhttp3.RequestBody.Companion.toRequestBody\nimport okio.source\nimport kotlinx.coroutines.Dispatchers\nimport kotlinx.coroutines.withContext\nimport com.example.BuildConfig\nimport java.util.UUID\nimport android.webkit.MimeTypeMap\nimport okhttp3.RequestBody.Companion.asRequestBody')

# Replace uploadImageToStorage and uploadBanner
pattern = re.compile(r'suspend fun uploadImageToStorage[\s\S]*?suspend fun setBannerUrlDirectly\(url: String\): String\? \{')

replacement = '''private val okHttpClient = OkHttpClient()

    private fun getMimeType(context: android.content.Context, uri: android.net.Uri): String {
        val extension = MimeTypeMap.getFileExtensionFromUrl(uri.toString())
        return MimeTypeMap.getSingleton().getMimeTypeFromExtension(extension)
            ?: context.contentResolver.getType(uri) ?: "image/jpeg"
    }

    suspend fun uploadImageToStorage(context: android.content.Context, uri: android.net.Uri, path: String): String? = withContext(Dispatchers.IO) {
        val supabaseUrl = BuildConfig.SUPABASE_URL
        val supabaseKey = BuildConfig.SUPABASE_ANON_KEY
        
        if (supabaseUrl.isEmpty() || supabaseKey.isEmpty()) {
            lastError = "Supabase não configurado"
            return@withContext null
        }

        try {
            val contentResolver = context.contentResolver
            val mimeType = getMimeType(context, uri)
            
            // Limit check (50MB)
            contentResolver.openFileDescriptor(uri, "r")?.use { pfd ->
                if (pfd.statSize > 50 * 1024 * 1024) {
                    lastError = "Imagem muito grande (máx 50MB)"
                    return@withContext null
                }
            }
            
            val inputStream = contentResolver.openInputStream(uri) ?: return@withContext null
            val bytes = inputStream.readBytes()
            inputStream.close()
            
            val requestBody = bytes.toRequestBody(mimeType.toMediaType())
            
            val url = "$supabaseUrl/storage/v1/object/nrdlojas-images/$path"
            
            val request = Request.Builder()
                .url(url)
                .post(requestBody) // Supabase uses POST for upload
                .addHeader("Authorization", "Bearer $supabaseKey")
                .addHeader("apikey", supabaseKey)
                .build()
                
            val response = okHttpClient.newCall(request).execute()
            if (response.isSuccessful) {
                return@withContext "$supabaseUrl/storage/v1/object/public/nrdlojas-images/$path"
            } else {
                Log.e("SupabaseStorage", "Error uploading: ${response.code} ${response.message} ${response.body?.string()}")
                lastError = "Falha no upload da imagem."
                return@withContext null
            }
        } catch (e: Exception) {
            Log.e("SupabaseStorage", "Exception uploading", e)
            lastError = e.message
            return@withContext null
        }
    }

    suspend fun uploadBanner(context: android.content.Context, uri: android.net.Uri): String? {
        return try {
            val extension = MimeTypeMap.getSingleton().getExtensionFromMimeType(getMimeType(context, uri)) ?: "jpg"
            val path = "banners/hero_banner_${System.currentTimeMillis()}.$extension"
            val downloadUrl = uploadImageToStorage(context, uri, path)
            if (downloadUrl != null) {
                if (isFirebaseConfigured()) {
                    val firestore = FirebaseFirestore.getInstance()
                    firestore.collection("config").document("appSettings")
                        .set(mapOf("bannerUrl" to downloadUrl)).await()
                }
            }
            downloadUrl
        } catch (e: Exception) {
            lastError = e.message
            Log.e("SupabaseStorage", "Error uploading banner", e)
            null
        }
    }

    suspend fun setBannerUrlDirectly(url: String): String? {'''

content = pattern.sub(replacement, content)

# Remove FirebaseStorage import
content = content.replace('import com.google.firebase.storage.FirebaseStorage', '')

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
    f.write(content)
print("Patched FirebaseService for Supabase Storage")
