sed -i '30,55d' app/src/main/java/com/example/data/FirebaseService.kt
sed -i '29a \
    suspend fun saveProduct(product: com.example.data.Product) {\
        if (!isFirebaseConfigured()) return\
        try {\
            val firestore = FirebaseFirestore.getInstance()\
            firestore.collection("products").document(product.code)\
                .set(mapOf(\
                    "code" to product.code,\
                    "name" to product.name,\
                    "searchName" to product.searchName,\
                    "category" to product.category,\
                    "unit" to product.unit,\
                    "imageUrl" to product.imageUrl,\
                    "searchCount" to product.searchCount,\
                    "timestamp" to System.currentTimeMillis()\
                )).await()\
            publishLatestProduct(product)\
        } catch (e: Exception) {\
            Log.e("FirebaseService", "Error saving product", e)\
        }\
    }\
\
    suspend fun syncAllProducts(products: List<com.example.data.Product>) {\
        if (!isFirebaseConfigured()) return\
        try {\
            val firestore = FirebaseFirestore.getInstance()\
            products.chunked(500).forEach { chunk ->\
                val batch = firestore.batch()\
                chunk.forEach { product ->\
                    val docRef = firestore.collection("products").document(product.code)\
                    batch.set(docRef, mapOf(\
                        "code" to product.code,\
                        "name" to product.name,\
                        "searchName" to product.searchName,\
                        "category" to product.category,\
                        "unit" to product.unit,\
                        "imageUrl" to product.imageUrl,\
                        "searchCount" to product.searchCount,\
                        "timestamp" to System.currentTimeMillis()\
                    ))\
                }\
                batch.commit().await()\
            }\
        } catch (e: Exception) {\
            Log.e("FirebaseService", "Error in syncAllProducts", e)\
        }\
    }' app/src/main/java/com/example/data/FirebaseService.kt
