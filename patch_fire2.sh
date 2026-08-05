sed -i '75a \
    suspend fun getAllProducts(): List<com.example.data.Product> {\
        if (!isFirebaseConfigured()) return emptyList()\
        return try {\
            val firestore = FirebaseFirestore.getInstance()' app/src/main/java/com/example/data/FirebaseService.kt
