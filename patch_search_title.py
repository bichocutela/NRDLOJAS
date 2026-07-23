import re

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "r") as f:
    content = f.read()

target = """            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .background(MaterialTheme.colorScheme.primary)
            )"""

replacement = """            Box(
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

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/SearchScreen.kt", "w") as f:
    f.write(content)
