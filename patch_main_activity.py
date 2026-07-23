import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import_code = """
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.ui.platform.LocalDensity
"""

content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier" + import_code)

theme_code = """
            val fontScale by userPreferences.fontScale.collectAsState(initial = 1.0f)
            val currentDensity = LocalDensity.current
            val customDensity = androidx.compose.ui.unit.Density(
                density = currentDensity.density,
                fontScale = currentDensity.fontScale * fontScale
            )

            CompositionLocalProvider(LocalDensity provides customDensity) {
                MyApplicationTheme {
"""

content = content.replace("setContent {\n            MyApplicationTheme {", "setContent {\n" + theme_code)

content = content.replace("                    }\n                }\n            }\n        }\n    }\n}", "                    }\n                }\n            }\n            }\n        }\n    }\n}")

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
