import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

helper = """
@Composable
fun StylizedText(
    text: String,
    baseStyle: TextStyle,
    largeText: Boolean,
    boldOutline: Boolean,
    uppercaseBold: Boolean,
    color: Color = Color.Unspecified,
    modifier: Modifier = Modifier
) {
    val finalText = if (uppercaseBold) text.uppercase() else text
    val weight = if (uppercaseBold || boldOutline) FontWeight.Bold else baseStyle.fontWeight
    val fontSize = if (largeText) baseStyle.fontSize * 1.3f else baseStyle.fontSize
    
    val styleWithMods = baseStyle.copy(
        fontWeight = weight,
        fontSize = fontSize,
        color = if (boldOutline) Color.Transparent else color
    )
    
    Box(modifier = modifier) {
        if (boldOutline) {
            androidx.compose.material3.Text(
                text = finalText,
                style = styleWithMods.copy(
                    drawStyle = Stroke(width = 2f)
                ),
                color = color
            )
        }
        androidx.compose.material3.Text(
            text = finalText,
            style = styleWithMods,
            color = if (boldOutline) Color.White else color
        )
    }
}
"""

if "fun StylizedText" not in content:
    content = content.replace("fun SearchScreen", helper + "\nfun SearchScreen")

# In ProductCard
product_card_old = """                Text(
                    text = product.name,
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold)
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = product.code,
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )"""
product_card_new = """                StylizedText(
                    text = product.name,
                    baseStyle = MaterialTheme.typography.titleMedium,
                    largeText = largeText,
                    boldOutline = boldOutline,
                    uppercaseBold = uppercaseBold,
                    color = MaterialTheme.colorScheme.onSurface
                )
                Spacer(modifier = Modifier.height(4.dp))
                StylizedText(
                    text = product.code,
                    baseStyle = MaterialTheme.typography.bodyMedium,
                    largeText = largeText,
                    boldOutline = boldOutline,
                    uppercaseBold = uppercaseBold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )"""
content = content.replace(product_card_old, product_card_new)

# In MiniProductCard
mini_product_old = """            Text(
                text = product.name,
                style = MaterialTheme.typography.labelMedium.copy(fontWeight = FontWeight.Bold),
                maxLines = 1,
                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
            )"""
mini_product_new = """            StylizedText(
                text = product.name,
                baseStyle = MaterialTheme.typography.labelMedium,
                largeText = largeText,
                boldOutline = boldOutline,
                uppercaseBold = uppercaseBold,
                color = MaterialTheme.colorScheme.onSurface
            )"""
content = content.replace(mini_product_old, mini_product_new)

# In HistoryItem
history_old = """            Text(
                text = product.name,
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.weight(1f)
            )"""
history_new = """            StylizedText(
                text = product.name,
                baseStyle = MaterialTheme.typography.bodyLarge,
                largeText = largeText,
                boldOutline = boldOutline,
                uppercaseBold = uppercaseBold,
                color = MaterialTheme.colorScheme.onSurface,
                modifier = Modifier.weight(1f)
            )"""
content = content.replace(history_old, history_new)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
