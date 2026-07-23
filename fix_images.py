import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

# Let's add crossfade and request building to AsyncImage
if "coil.request.ImageRequest" not in content:
    content = content.replace("import coil.compose.AsyncImage", "import coil.compose.AsyncImage\nimport coil.request.ImageRequest\nimport androidx.compose.ui.platform.LocalContext")

old_async1 = """                AsyncImage(
                    model = product.imageUrl,
                    contentDescription = product.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(48.dp)
                        .clip(CircleShape)
                )"""

new_async1 = """                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(product.imageUrl)
                        .crossfade(true)
                        .build(),
                    contentDescription = product.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(48.dp)
                        .clip(CircleShape)
                )"""

old_async2 = """                AsyncImage(
                    model = product.imageUrl,
                    contentDescription = product.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                )"""

new_async2 = """                AsyncImage(
                    model = ImageRequest.Builder(LocalContext.current)
                        .data(product.imageUrl)
                        .crossfade(true)
                        .build(),
                    contentDescription = product.name,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                )"""

content = content.replace(old_async1, new_async1)
content = content.replace(old_async2, new_async2)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
