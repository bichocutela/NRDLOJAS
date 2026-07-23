import re

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

if "import coil.compose.AsyncImage" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import coil.compose.AsyncImage\nimport androidx.compose.ui.layout.ContentScale\nimport androidx.compose.foundation.shape.CircleShape\nimport androidx.compose.ui.draw.clip\nimport androidx.compose.foundation.background\nimport androidx.compose.ui.Alignment")

row_replace = """            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                if (product.imageUrl != null) {
                    AsyncImage(
                        model = product.imageUrl,
                        contentDescription = product.name,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier
                            .size(40.dp)
                            .clip(CircleShape)
                    )
                } else {
                    Box(
                        modifier = Modifier
                            .size(40.dp)
                            .clip(CircleShape)
                            .background(MaterialTheme.colorScheme.primaryContainer),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = product.name.take(1).uppercase(),
                            style = MaterialTheme.typography.titleMedium,
                            color = MaterialTheme.colorScheme.onPrimaryContainer
                        )
                    }
                }
                Spacer(modifier = Modifier.width(16.dp))
                Text(text = product.name, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.weight(1f))
                IconButton(onClick = { isEditing = !isEditing }) {
                    Icon(if (isEditing) Icons.Default.Close else Icons.Default.Edit, contentDescription = "Editar")
                }
            }"""

content = re.sub(r"            Row\(\s*modifier = Modifier\.fillMaxWidth\(\),\s*horizontalArrangement = Arrangement\.SpaceBetween,\s*verticalAlignment = Alignment\.CenterVertically\s*\)\s*\{\s*Text\(text = product\.name, style = MaterialTheme\.typography\.bodyLarge, modifier = Modifier\.weight\(1f\)\)\s*IconButton\(onClick = \{ isEditing = !isEditing \}\)\s*\{\s*Icon\(if \(isEditing\) Icons\.Default\.Close else Icons\.Default\.Edit, contentDescription = \"Editar\"\)\s*\}\s*\}", row_replace, content)

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "w") as f:
    f.write(content)
