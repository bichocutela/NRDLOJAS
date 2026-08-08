import re

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'r') as f:
    content = f.read()

# Replace uploadBanner
pattern_banner = re.compile(r'suspend fun uploadBanner\(context: android\.content\.Context, uri: Uri\): String\? \{[\s\S]*?val firestore = FirebaseFirestore\.getInstance\(\)\s*firestore\.collection\("config"\)\.document\("appSettings"\)\s*\.set\(mapOf\("bannerUrl" to dataUrl\)\)\.await\(\)\s*dataUrl\s*\} catch \(e: Exception\) \{\s*lastError = e\.message\s*Log\.e\("FirebaseService", "Error uploading banner", e\)\s*null\s*\}\s*\}')

replacement_banner = '''suspend fun uploadImageToStorage(uri: Uri, path: String): String? {
        if (!isFirebaseConfigured()) return null
        return try {
            val storage = FirebaseStorage.getInstance()
            val ref = storage.reference.child(path)
            ref.putFile(uri).await()
            ref.downloadUrl.await().toString()
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error uploading to storage", e)
            null
        }
    }

    suspend fun uploadBanner(context: android.content.Context, uri: Uri): String? {
        if (!isFirebaseConfigured()) {
            lastError = "Firebase not configured (initialize failed?)"
            return null
        }
        return try {
            val downloadUrl = uploadImageToStorage(uri, "banners/hero_banner_${System.currentTimeMillis()}.jpg")
            if (downloadUrl != null) {
                val firestore = FirebaseFirestore.getInstance()
                firestore.collection("config").document("appSettings")
                    .set(mapOf("bannerUrl" to downloadUrl)).await()
            }
            downloadUrl
        } catch (e: Exception) {
            lastError = e.message
            Log.e("FirebaseService", "Error uploading banner", e)
            null
        }
    }
'''

content = pattern_banner.sub(replacement_banner, content)

# Add deleteProduct
pattern_save = re.compile(r'suspend fun saveProduct\(product: com\.example\.data\.Product\) \{[\s\S]*?publishLatestProduct\(product\)\s*\} catch \(e: Exception\) \{\s*Log\.e\("FirebaseService", "Error saving product", e\)\s*\}\s*\}')

replacement_save = '''suspend fun saveProduct(product: com.example.data.Product) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("products").document(product.code)
                .set(mapOf(
                    "code" to product.code,
                    "name" to product.name,
                    "searchName" to product.searchName,
                    "category" to product.category,
                    "unit" to product.unit,
                    "imageUrl" to product.imageUrl,
                    "searchCount" to product.searchCount,
                    "timestamp" to System.currentTimeMillis()
                )).await()
            publishLatestProduct(product)
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error saving product", e)
        }
    }
    
    suspend fun deleteProduct(code: String) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("products").document(code).delete().await()
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error deleting product", e)
        }
    }
'''
content = pattern_save.sub(replacement_save, content)

# Add observeProducts
pattern_observe_latest = re.compile(r'fun observeLatestProduct\(\): Flow<Map<String, Any>\?> = callbackFlow \{')

replacement_observe_latest = '''fun observeProducts(): Flow<List<com.example.data.Product>> = callbackFlow {
        if (!isFirebaseConfigured()) {
            trySend(emptyList())
            close()
            return@callbackFlow
        }
        val firestore = FirebaseFirestore.getInstance()
        val registration = firestore.collection("products")
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    trySend(emptyList())
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val products = snapshot.documents.mapNotNull { doc ->
                        val code = doc.getString("code") ?: return@mapNotNull null
                        val name = doc.getString("name") ?: ""
                        val searchName = doc.getString("searchName") ?: ""
                        val category = doc.getString("category") ?: ""
                        val unit = doc.getString("unit") ?: "un"
                        val imageUrl = doc.getString("imageUrl")
                        val searchCount = doc.getLong("searchCount")?.toInt() ?: 0
                        com.example.data.Product(
                            code = code,
                            name = name,
                            searchName = searchName,
                            category = category,
                            unit = unit,
                            imageUrl = imageUrl,
                            searchCount = searchCount
                        )
                    }
                    trySend(products)
                }
            }
        awaitClose { registration.remove() }
    }

    fun observeLatestProduct(): Flow<Map<String, Any>?> = callbackFlow {'''
content = pattern_observe_latest.sub(replacement_observe_latest, content)

with open('app/src/main/java/com/example/data/FirebaseService.kt', 'w') as f:
    f.write(content)
print("Patched FirebaseService")
