import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

icon_target = """                                Icon(
                                    imageVector = Icons.Default.ShoppingCart,
                                    contentDescription = "Logo",
                                    tint = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.size(150.dp)
                                )"""
                                
image_repl = """                                Image(
                                    painter = painterResource(id = R.drawable.splash_logo),
                                    contentDescription = "Logo",
                                    modifier = Modifier.size(150.dp)
                                )"""

content = content.replace(icon_target, image_repl)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content2 = f.read()

box_target = """            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.primary),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "NRD Códigos Correlatos",
                    style = MaterialTheme.typography.headlineMedium,
                    color = MaterialTheme.colorScheme.onPrimary
                )
            }"""
            
box_repl = """            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Image(
                    painter = painterResource(id = R.drawable.hero_banner),
                    contentDescription = "Banner Nordestão",
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                Text(
                    text = "NRD Códigos Correlatos",
                    style = MaterialTheme.typography.headlineMedium,
                    color = MaterialTheme.colorScheme.onPrimary
                )
            }"""
            
content2 = content2.replace(box_target, box_repl)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content2)

