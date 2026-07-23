import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

imports = """import androidx.compose.foundation.Image
import androidx.compose.ui.res.painterResource
"""
if "import androidx.compose.ui.res.painterResource" not in content:
    content = content.replace("import androidx.compose.foundation.layout.Box", "import androidx.compose.foundation.layout.Box\n" + imports)

old_icon = """                                Icon(
                                    imageVector = Icons.Default.Favorite,
                                    contentDescription = "Logo",
                                    tint = Color.Red,
                                    modifier = Modifier.size(100.dp)
                                )"""

new_icon = """                                Image(
                                    painter = painterResource(id = R.drawable.logo_nordestao),
                                    contentDescription = "Logo",
                                    modifier = Modifier.size(150.dp)
                                )"""

content = content.replace(old_icon, new_icon)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
