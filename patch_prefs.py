import re

with open("app/src/main/java/com/example/data/UserPreferences.kt", "r") as f:
    content = f.read()

import_float = "import androidx.datastore.preferences.core.floatPreferencesKey\n"
content = content.replace("import androidx.datastore.preferences.core.booleanPreferencesKey", "import androidx.datastore.preferences.core.booleanPreferencesKey\n" + import_float)

font_scale_flow = """
    val fontScale: Flow<Float> = context.dataStore.data.map { preferences ->
        preferences[FONT_SCALE] ?: 1.0f
    }
"""

content = content.replace("val notificationsEnabled:", font_scale_flow.strip() + "\n    val notificationsEnabled:")

font_scale_setter = """
    suspend fun setFontScale(scale: Float) {
        context.dataStore.edit { it[FONT_SCALE] = scale }
    }
"""

content = content.replace("suspend fun setNotificationsEnabled(enabled: Boolean) {", font_scale_setter.strip() + "\n    suspend fun setNotificationsEnabled(enabled: Boolean) {")

content = content.replace("val NOTIFICATIONS_ENABLED = booleanPreferencesKey(\"notifications_enabled\")", "val NOTIFICATIONS_ENABLED = booleanPreferencesKey(\"notifications_enabled\")\n        val FONT_SCALE = floatPreferencesKey(\"font_scale\")")

with open("app/src/main/java/com/example/data/UserPreferences.kt", "w") as f:
    f.write(content)
