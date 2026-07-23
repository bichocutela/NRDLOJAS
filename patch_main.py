import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

import_cart = "import androidx.compose.material.icons.filled.ShoppingCart"
content = content.replace("import androidx.compose.material.icons.filled.Favorite", import_cart + "\nimport androidx.compose.material.icons.filled.Favorite")

image_code = """
                                Icon(
                                    imageVector = Icons.Default.ShoppingCart,
                                    contentDescription = "Logo",
                                    tint = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(150.dp)
                                )
"""

content = re.sub(r'Image\(\s*painter\s*=\s*painterResource\(id\s*=\s*R\.drawable\.splash_logo\),\s*contentDescription\s*=\s*"Logo",\s*modifier\s*=\s*Modifier\.size\(150\.dp\)\s*\)', image_code.strip(), content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
