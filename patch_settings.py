import re

with open("app/src/main/java/com/example/ui/SettingsScreen.kt", "r") as f:
    content = f.read()

theme_ui = """
            Text("Tema do Aplicativo", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.primary)
            
            val appTheme by viewModel.userPreferences.appTheme.collectAsState(initial = "red")
            var expandedThemeMenu by remember { mutableStateOf(false) }
            val themeOptions = listOf(
                "red" to "Vermelho (Padrão)",
                "gold" to "Dourado",
                "green" to "Verde",
                "blue" to "Azul",
                "orange" to "Laranja"
            )
            
            ExposedDropdownMenuBox(
                expanded = expandedThemeMenu,
                onExpandedChange = { expandedThemeMenu = !expandedThemeMenu }
            ) {
                OutlinedTextField(
                    value = themeOptions.find { it.first == appTheme }?.second ?: "Vermelho (Padrão)",
                    onValueChange = {},
                    readOnly = true,
                    label = { Text("Selecione o Tema") },
                    trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expandedThemeMenu) },
                    modifier = Modifier.menuAnchor().fillMaxWidth(),
                    colors = ExposedDropdownMenuDefaults.outlinedTextFieldColors()
                )
                ExposedDropdownMenu(
                    expanded = expandedThemeMenu,
                    onDismissRequest = { expandedThemeMenu = false }
                ) {
                    themeOptions.forEach { (themeKey, themeLabel) ->
                        DropdownMenuItem(
                            text = { Text(themeLabel) },
                            onClick = {
                                coroutineScope.launch { viewModel.userPreferences.setAppTheme(themeKey) }
                                expandedThemeMenu = false
                            }
                        )
                    }
                }
            }
            
            HorizontalDivider()
"""

if "Tema do Aplicativo" not in content:
    content = content.replace("Text(\"Vibração\",", theme_ui + "\n            Text(\"Vibração\",")
    with open("app/src/main/java/com/example/ui/SettingsScreen.kt", "w") as f:
        f.write(content)
    print("Patched SettingsScreen")
else:
    print("Already patched SettingsScreen")
