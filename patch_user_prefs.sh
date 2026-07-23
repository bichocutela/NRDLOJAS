sed -i '/val notificationsEnabled/i \
    val bannerImageUri: Flow<String?> = context.dataStore.data.map { preferences ->\
        preferences[BANNER_IMAGE_URI]\
    }' app/src/main/java/com/example/data/UserPreferences.kt

sed -i '/suspend fun setNotificationsEnabled/i \
    suspend fun setBannerImageUri(uri: String?) {\
        context.dataStore.edit { if (uri == null) it.remove(BANNER_IMAGE_URI) else it[BANNER_IMAGE_URI] = uri }\
    }' app/src/main/java/com/example/data/UserPreferences.kt

sed -i '/val FONT_SCALE/a \
        val BANNER_IMAGE_URI = stringPreferencesKey("banner_image_uri")' app/src/main/java/com/example/data/UserPreferences.kt
