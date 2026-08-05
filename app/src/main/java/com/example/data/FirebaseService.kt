package com.example.data

import android.net.Uri
import com.google.firebase.FirebaseApp
import com.google.firebase.firestore.FirebaseFirestore
import com.google.firebase.storage.FirebaseStorage
import kotlinx.coroutines.tasks.await
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import kotlinx.coroutines.channels.awaitClose
import android.util.Log

object FirebaseService {
    var lastError: String? = null
    suspend fun publishLatestProduct(product: com.example.data.Product) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("latest_product").document("latest")
                .set(mapOf(
                    "name" to product.name,
                    "code" to product.code,
                    "timestamp" to System.currentTimeMillis()
                )).await()
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error publishing latest product", e)
        }
    }

    suspend fun saveProduct(product: com.example.data.Product) {
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

    suspend fun syncAllProducts(products: List<com.example.data.Product>) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            products.chunked(500).forEach { chunk ->
                val batch = firestore.batch()
                chunk.forEach { product ->
                    val docRef = firestore.collection("products").document(product.code)
                    batch.set(docRef, mapOf(
                        "code" to product.code,
                        "name" to product.name,
                        "searchName" to product.searchName,
                        "category" to product.category,
                        "unit" to product.unit,
                        "imageUrl" to product.imageUrl,
                        "searchCount" to product.searchCount,
                        "timestamp" to System.currentTimeMillis()
                    ))
                }
                batch.commit().await()
            }
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error in syncAllProducts", e)
        }
    }
    suspend fun getAllProducts(): List<com.example.data.Product> {
        if (!isFirebaseConfigured()) return emptyList()
        return try {
            val firestore = FirebaseFirestore.getInstance()
            val snapshot = firestore.collection("products").get().await()
            snapshot.documents.mapNotNull { doc ->
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
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error fetching products", e)
            emptyList()
        }
    }

    fun observeLatestProduct(): Flow<Map<String, Any>?> = callbackFlow {
        if (!isFirebaseConfigured()) {
            trySend(null)
            close()
            return@callbackFlow
        }
        val firestore = FirebaseFirestore.getInstance()
        val registration = firestore.collection("latest_product").document("latest")
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    trySend(null)
                    return@addSnapshotListener
                }
                if (snapshot != null && snapshot.exists()) {
                    trySend(snapshot.data)
                } else {
                    trySend(null)
                }
            }
        awaitClose { registration.remove() }
    }
    
    fun isFirebaseConfigured(): Boolean {
        return try {
            FirebaseApp.getInstance()
            true
        } catch (e: Exception) {
            false
        }
    }
    
    fun initialize(context: android.content.Context) {
        try {
            FirebaseApp.getInstance()
            try {
                val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
                if (auth.currentUser == null) {
                    auth.signInAnonymously()
                }
            } catch (e: Exception) {
            }
        } catch (e: Exception) {
            val rawApiKey = com.example.BuildConfig.FIREBASE_API_KEY
            val rawProjectId = com.example.BuildConfig.FIREBASE_PROJECT_ID
            val rawAppId = com.example.BuildConfig.FIREBASE_APP_ID
                        
            if (rawApiKey != "dummy" && rawProjectId != "dummy" && rawAppId != "dummy") {
                // Corrigir possível inversão de Project ID e App ID no painel de secrets
                val apiKey = rawApiKey
                val appId = if (rawProjectId.contains(":") && !rawAppId.contains(":")) rawProjectId else rawAppId
                val projectId = if (rawProjectId.contains(":") && !rawAppId.contains(":")) rawAppId else rawProjectId
                
                try {
                    val options = com.google.firebase.FirebaseOptions.Builder()
                        .setApiKey(apiKey)
                        .setProjectId(projectId)
                        .setApplicationId(appId)
                        .setStorageBucket(projectId + ".appspot.com")
                        .build()
                    FirebaseApp.initializeApp(context, options)
                    
                    try {
                        com.google.firebase.auth.FirebaseAuth.getInstance().signInAnonymously()
                    } catch (e: Exception) {
                        Log.e("FirebaseService", "Auth error", e)
                    }
                } catch (ex: Exception) {
                    lastError = "Init error: " + ex.message
                    Log.e("FirebaseService", "Erro ao inicializar Firebase", ex)
                }
            }
        }
    }

    suspend fun uploadBanner(context: android.content.Context, uri: Uri): String? {
        if (!isFirebaseConfigured()) {
            lastError = "Firebase not configured (initialize failed?)"
            return null
        }
        return try {
            val inputStream = context.contentResolver.openInputStream(uri)
            val bitmap = android.graphics.BitmapFactory.decodeStream(inputStream)
            inputStream?.close()

            val maxW = 1024
            val maxH = 1024
            val scaledBitmap = if (bitmap.width > maxW || bitmap.height > maxH) {
                val ratio = Math.min(maxW.toFloat() / bitmap.width, maxH.toFloat() / bitmap.height)
                android.graphics.Bitmap.createScaledBitmap(bitmap, (bitmap.width * ratio).toInt(), (bitmap.height * ratio).toInt(), true)
            } else {
                bitmap
            }

            val baos = java.io.ByteArrayOutputStream()
            scaledBitmap.compress(android.graphics.Bitmap.CompressFormat.JPEG, 60, baos)
            val base64Data = android.util.Base64.encodeToString(baos.toByteArray(), android.util.Base64.NO_WRAP)
            val dataUrl = "data:image/jpeg;base64,$base64Data"
            
            // Save to Firestore
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("config").document("appSettings")
                .set(mapOf("bannerUrl" to dataUrl)).await()
                
            dataUrl
        } catch (e: Exception) {
            lastError = e.message
            Log.e("FirebaseService", "Error uploading banner", e)
            null
        }
    }

    suspend fun setBannerUrlDirectly(url: String): String? {
        if (!isFirebaseConfigured()) {
            lastError = "Firebase not configured"
            return url
        }
        return try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("config").document("appSettings")
                .set(mapOf("bannerUrl" to url)).await()
            url
        } catch (e: Exception) {
            lastError = e.message
            url
        }
    }
    suspend fun getBannerUrl(): String? {
        if (!isFirebaseConfigured()) return null
        return try {
            val firestore = FirebaseFirestore.getInstance()
            val snapshot = firestore.collection("config").document("appSettings").get().await()
            snapshot.getString("bannerUrl")
        } catch (e: Exception) {
            null
        }
    }
    fun observeBannerUrl(): Flow<String?> = callbackFlow {
        if (!isFirebaseConfigured()) {
            trySend(null)
            close()
            return@callbackFlow
        }
        
        val firestore = FirebaseFirestore.getInstance()
        val registration = firestore.collection("config").document("appSettings")
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    Log.e("FirebaseService", "Listen failed.", error)
                    trySend(null)
                    return@addSnapshotListener
                }
                
                if (snapshot != null && snapshot.exists()) {
                    val url = snapshot.getString("bannerUrl")
                    trySend(url)
                } else {
                    trySend(null)
                }
            }
            
        awaitClose { registration.remove() }
    }
}
