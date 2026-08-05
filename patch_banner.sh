sed -i '215a \
    suspend fun getBannerUrl(): String? {\
        if (!isFirebaseConfigured()) return null\
        return try {\
            val firestore = FirebaseFirestore.getInstance()\
            val snapshot = firestore.collection("config").document("appSettings").get().await()\
            snapshot.getString("bannerUrl")\
        } catch (e: Exception) {\
            null\
        }\
    }' app/src/main/java/com/example/data/FirebaseService.kt
