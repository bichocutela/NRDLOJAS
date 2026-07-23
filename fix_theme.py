import re

with open("app/src/main/java/com/example/ui/theme/Color.kt", "w") as f:
    f.write("""package com.example.ui.theme

import androidx.compose.ui.graphics.Color

val NordestaoRed = Color(0xFFE62325)
val NordestaoRedDark = Color(0xFFC01518)
val NordestaoYellow = Color(0xFFF0A72F)
val NordestaoYellowLight = Color(0xFFFDE8C7)
val NordestaoBlue = Color(0xFF1976D2)
val NordestaoGreen = Color(0xFF388E3C)

val BackgroundWhite = Color(0xFFFFFFFF)
val SurfaceWhite = Color(0xFFF7F7F7)
val TextPrimary = Color(0xFF212121)
val TextSecondary = Color(0xFF757575)
val OutlineColor = Color(0xFFE0E0E0)
""")

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write("""package com.example.ui.theme

import android.os.Build
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext

private val LightColorScheme = lightColorScheme(
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

@Composable
fun MyApplicationTheme(
    darkTheme: Boolean = false,
    // Dynamic color is available on Android 12+
    dynamicColor: Boolean = false, // Disabled dynamic color to strictly use our palette
    content: @Composable () -> Unit
) {
    val colorScheme = LightColorScheme

    MaterialTheme(colorScheme = colorScheme, typography = Typography, content = content)
}
""")
