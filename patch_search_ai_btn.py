import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

product_card_btn = """
        Spacer(modifier = Modifier.width(8.dp))
        androidx.compose.material3.IconButton(
            onClick = { viewModel.consultProductInfoAi(product) },
            modifier = Modifier.background(MaterialTheme.colorScheme.tertiaryContainer, CircleShape)
        ) {
            Icon(Icons.Default.AutoAwesome, contentDescription = "IA Info", tint = MaterialTheme.colorScheme.onTertiaryContainer)
        }
    }
}
"""

content = content.replace("            }\n        }\n    }\n}\n\n@Composable\nfun MiniProductCard", "            }\n        }\n" + product_card_btn + "\n\n@Composable\nfun MiniProductCard")

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
