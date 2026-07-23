package com.example.data

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.floatPreferencesKey

import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "settings")

class UserPreferences(private val context: Context) {

    val vibrateOnClick: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[VIBRATE_ON_CLICK] ?: true
    }

    val vibrateOnFound: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[VIBRATE_ON_FOUND] ?: true
    }

    val largeText: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[LARGE_TEXT] ?: false
    }

    val boldOutline: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[BOLD_OUTLINE] ?: false
    }

    val uppercaseBold: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[UPPERCASE_BOLD] ?: false
    }

    val fontScale: Flow<Float> = context.dataStore.data.map { preferences ->
        preferences[FONT_SCALE] ?: 1.0f
    }
    val notificationsEnabled: Flow<Boolean> = context.dataStore.data.map { preferences ->
        preferences[NOTIFICATIONS_ENABLED] ?: true
    }

    suspend fun setVibrateOnClick(enabled: Boolean) {
        context.dataStore.edit { it[VIBRATE_ON_CLICK] = enabled }
    }

    suspend fun setVibrateOnFound(enabled: Boolean) {
        context.dataStore.edit { it[VIBRATE_ON_FOUND] = enabled }
    }

    suspend fun setLargeText(enabled: Boolean) {
        context.dataStore.edit { it[LARGE_TEXT] = enabled }
    }

    suspend fun setBoldOutline(enabled: Boolean) {
        context.dataStore.edit { it[BOLD_OUTLINE] = enabled }
    }

    suspend fun setUppercaseBold(enabled: Boolean) {
        context.dataStore.edit { it[UPPERCASE_BOLD] = enabled }
    }

    suspend fun setFontScale(scale: Float) {
        context.dataStore.edit { it[FONT_SCALE] = scale }
    }
    suspend fun setNotificationsEnabled(enabled: Boolean) {
        context.dataStore.edit { it[NOTIFICATIONS_ENABLED] = enabled }
    }

    companion object {
        val VIBRATE_ON_CLICK = booleanPreferencesKey("vibrate_on_click")
        val VIBRATE_ON_FOUND = booleanPreferencesKey("vibrate_on_found")
        val LARGE_TEXT = booleanPreferencesKey("large_text")
        val BOLD_OUTLINE = booleanPreferencesKey("bold_outline")
        val UPPERCASE_BOLD = booleanPreferencesKey("uppercase_bold")
        val NOTIFICATIONS_ENABLED = booleanPreferencesKey("notifications_enabled")
        val FONT_SCALE = floatPreferencesKey("font_scale")
    }
}
