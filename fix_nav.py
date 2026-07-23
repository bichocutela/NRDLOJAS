with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "r") as f:
    content = f.read()

target = """        Spacer(modifier = Modifier.height(24.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Categorias","""

replacement = """        Spacer(modifier = Modifier.height(24.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(16.dp))
        
        Button(
            onClick = onGoToSettings,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Configurações")
        }
        
        Spacer(modifier = Modifier.height(24.dp))
        HorizontalDivider()
        Spacer(modifier = Modifier.height(16.dp))
        
        Text(
            text = "Categorias","""

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/AppNavGraph.kt", "w") as f:
    f.write(content)
