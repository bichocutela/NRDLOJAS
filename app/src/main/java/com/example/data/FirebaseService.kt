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
            if (products.isNotEmpty()) {
                val latest = products.maxByOrNull { it.id }
                if (latest != null) publishLatestProduct(latest)
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
            val auth = com.google.firebase.auth.FirebaseAuth.getInstance()
            if (auth.currentUser == null) {
                auth.signInAnonymously()
            }
        } catch (e: Exception) {
            Log.e("FirebaseService", "Auth error", e)
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


    suspend fun syncAllDynamicTabs(tabs: List<com.example.data.DynamicTab>) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            val batch = firestore.batch()
            tabs.forEach { tab ->
                val docRef = firestore.collection("dynamic_tabs").document(tab.id.toString())
                batch.set(docRef, mapOf(
                    "id" to tab.id,
                    "title" to tab.title,
                    "type" to tab.type,
                    "content" to tab.content,
                    "displayOrder" to tab.displayOrder
                ))
            }
            batch.commit().await()
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error syncing dynamic tabs", e)
        }
    }

    suspend fun deleteDynamicTab(tab: com.example.data.DynamicTab) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("dynamic_tabs").document(tab.id.toString())
                .delete().await()
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error deleting dynamic tab", e)
        }
    }

    fun observeDynamicTabs(): Flow<List<com.example.data.DynamicTab>> = callbackFlow {
        if (!isFirebaseConfigured()) {
            trySend(emptyList())
            close()
            return@callbackFlow
        }
        val firestore = FirebaseFirestore.getInstance()
        val registration = firestore.collection("dynamic_tabs")
            .addSnapshotListener { snapshot, error ->
                if (error != null) {
                    trySend(emptyList())
                    return@addSnapshotListener
                }
                if (snapshot != null) {
                    val tabs = snapshot.documents.mapNotNull { doc ->
                        val id = doc.getLong("id")?.toInt() ?: return@mapNotNull null
                        val title = doc.getString("title") ?: ""
                        val type = doc.getString("type") ?: ""
                        val content = doc.getString("content") ?: ""
                        val displayOrder = doc.getLong("displayOrder")?.toInt() ?: 0
                        com.example.data.DynamicTab(
                            id = id,
                            title = title,
                            type = type,
                            content = content,
                            displayOrder = displayOrder
                        )
                    }
                    trySend(tabs)
                }
            }
        awaitClose { registration.remove() }
    }
}
