import re

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    content = f.read()

pattern = re.compile(r'suspend fun uploadImageToStorage[\s\S]*?suspend fun uploadBanner')

replacement = '''suspend fun uploadImageToStorage(uri: android.net.Uri, path: String): String? = withContext(Dispatchers.IO) {
        val supabaseUrl = BuildConfig.SUPABASE_URL
        val supabaseKey = BuildConfig.SUPABASE_ANON_KEY
        
        if (supabaseUrl.isEmpty() || supabaseKey.isEmpty()) {
            lastError = "Supabase não configurado"
            return@withContext null
        }
        
        val currentUser = com.google.firebase.auth.FirebaseAuth.getInstance().currentUser
        if (currentUser == null) {
            lastError = "Usuário não autenticado no Firebase Auth"
            return@withContext null
        }
        
        val firebaseToken = try {
            currentUser.getIdToken(false).await().token
        } catch (e: Exception) {
            lastError = "Erro ao obter token do Firebase"
            return@withContext null
        }
        
        if (firebaseToken == null) {
            lastError = "Token do Firebase nulo"
            return@withContext null
        }

        try {
            val ctx = appContext ?: return@withContext null
            val contentResolver = ctx.contentResolver
            val mimeType = getMimeType(ctx, uri)
            
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
            
            val requestBody = okhttp3.MultipartBody.Builder()
                .setType(okhttp3.MultipartBody.FORM)
                .addFormDataPart("path", path)
                .addFormDataPart("file", "image.jpg", bytes.toRequestBody(mimeType.toMediaType()))
                .build()
            
            val url = "$supabaseUrl/functions/v1/upload-image"
            
            val request = Request.Builder()
                .url(url)
                .post(requestBody) 
                .addHeader("Authorization", "Bearer $supabaseKey")
                .addHeader("x-firebase-token", firebaseToken)
                .build()
                
            val response = okHttpClient.newCall(request).execute()
            if (response.isSuccessful) {
                val responseStr = response.body?.string()
                try {
                    if (responseStr != null) {
                        val json = org.json.JSONObject(responseStr)
                        if (json.has("url")) {
                            return@withContext json.getString("url")
                        }
                    }
                } catch (e: Exception) {
                    Log.e("SupabaseStorage", "Error parsing response", e)
                }
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

    suspend fun uploadBanner'''

content = pattern.sub(replacement, content)

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
    f.write(content)
print("Patched FirebaseService for Edge Function")
