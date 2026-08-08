import re

with open("app/src/main/java/com/example/data/UserPreferences.kt", "r") as f:
    content = f.read()

if "appTheme: Flow<String>" not in content:
    content = content.replace("val onboardingShown:", "val appTheme: Flow<String> = context.dataStore.data.map { preferences ->\n        preferences[APP_THEME] ?: \"red\"\n    }\n\n    val onboardingShown:")
    content = content.replace("suspend fun setOnboardingShown(", "suspend fun setAppTheme(theme: String) {\n        context.dataStore.edit { it[APP_THEME] = theme }\n    }\n\n    suspend fun setOnboardingShown(")
    content = content.replace("val ONBOARDING_SHOWN =", "val APP_THEME = stringPreferencesKey(\"app_theme\")\n        val ONBOARDING_SHOWN =")
    
    with open("app/src/main/java/com/example/data/UserPreferences.kt", "w") as f:
        f.write(content)
    print("Patched UserPreferences")
