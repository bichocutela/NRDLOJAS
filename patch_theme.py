import re

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    content = f.read()

replacement = """package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

private val DefaultLightColorScheme = lightColorScheme(
    primary = NordestaoRed,
    onPrimary = Color.White,
    primaryContainer = NordestaoRedDark,
    onPrimaryContainer = Color.White,
    secondary = NordestaoYellow,
    onSecondary = TextPrimary,
    secondaryContainer = NordestaoYellowLight,
    onSecondaryContainer = TextPrimary,
    tertiary = NordestaoBlue,
    onTertiary = Color.White,
    background = BackgroundWhite,
    onBackground = TextPrimary,
    surface = SurfaceWhite,
    onSurface = TextPrimary,
    surfaceVariant = Color(0xFFF0F0F0),
    onSurfaceVariant = TextSecondary,
    outline = OutlineColor
)

private fun getThemeColorScheme(themeName: String) = when(themeName) {
    "gold" -> DefaultLightColorScheme.copy(
        primary = Color(0xFFD4AF37),
        primaryContainer = Color(0xFFB8952B),
        onPrimary = Color.White,
        onPrimaryContainer = Color.White
    )
    "green" -> DefaultLightColorScheme.copy(
        primary = Color(0xFF388E3C),
        primaryContainer = Color(0xFF2E7D32),
        onPrimary = Color.White,
        onPrimaryContainer = Color.White
    )
    "blue" -> DefaultLightColorScheme.copy(
        primary = Color(0xFF1976D2),
        primaryContainer = Color(0xFF1565C0),
        onPrimary = Color.White,
        onPrimaryContainer = Color.White
    )
    "orange" -> DefaultLightColorScheme.copy(
        primary = Color(0xFFFF9800),
        primaryContainer = Color(0xFFF57C00),
        onPrimary = Color.White,
        onPrimaryContainer = Color.White
    )
    else -> DefaultLightColorScheme
}

@Composable
fun MyApplicationTheme(
    appTheme: String = "red",
    darkTheme: Boolean = false,
    dynamicColor: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = getThemeColorScheme(appTheme)
    MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
"""

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(replacement)
print("Patched Theme.kt")
