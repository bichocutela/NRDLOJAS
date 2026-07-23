import re

with open("app/src/main/java/com/example/ui/SettingsScreen.kt", "r") as f:
    content = f.read()

content = content.replace("val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)", "val largeText by viewModel.userPreferences.largeText.collectAsState(initial = false)\n    val fontScale by viewModel.userPreferences.fontScale.collectAsState(initial = 1.0f)")

slider_ui = """
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text("Tamanho da Fonte", modifier = Modifier.weight(1f))
                Slider(
                    value = fontScale,
                    onValueChange = { coroutineScope.launch { viewModel.userPreferences.setFontScale(it) } },
                    valueRange = 0.8f..2.0f,
                    steps = 11,
                    modifier = Modifier.weight(2f).padding(horizontal = 16.dp)
                )
                Text(String.format("%.1fx", fontScale))
            }
            Button(onClick = { coroutineScope.launch { viewModel.userPreferences.setFontScale(1.0f) } }, modifier = Modifier.align(Alignment.End)) {
                Text("Restaurar Padrão")
            }
"""

content = content.replace("Text(\"Preferências de Interface\", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)", "Text(\"Preferências de Interface\", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)\n" + slider_ui)

with open("app/src/main/java/com/example/ui/SettingsScreen.kt", "w") as f:
    f.write(content)
