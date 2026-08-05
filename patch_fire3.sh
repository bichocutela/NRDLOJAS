sed -i '215a \
    suspend fun setBannerUrlDirectly(url: String): String? {\
        if (!isFirebaseConfigured()) {\
            lastError = "Firebase not configured"\
            return url\
        }\
        return try {\
            val firestore = FirebaseFirestore.getInstance()\
            firestore.collection("config").document("appSettings")\
                .set(mapOf("bannerUrl" to url)).await()\
            url\
        } catch (e: Exception) {\
            lastError = e.message\
            url\
        }\
    }' app/src/main/java/com/example/data/FirebaseService.kt
