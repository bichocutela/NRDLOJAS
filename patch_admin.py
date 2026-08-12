import sys
with open("app/src/main/java/com/example/ui/AdminScreen.kt", "r") as f:
    content = f.read()

if "import com.example.ui.theme.getDynamicThemeColor" not in content:
    content = content.replace("import androidx.compose.ui.Modifier", "import androidx.compose.ui.Modifier\nimport com.example.ui.theme.getDynamicThemeColor")

# Add appTheme collection
content = content.replace('val isSyncing by viewModel.isSyncing.collectAsStateWithLifecycle()', 'val isSyncing by viewModel.isSyncing.collectAsStateWithLifecycle()\n    val appTheme by viewModel.userPreferences.appTheme.collectAsStateWithLifecycle(initialValue = "multicolor")')

# Exportar Inventário
target_btn1 = """                    onClick = {
                        scope.launch {"""
replacement_btn1 = """                    colors = ButtonDefaults.buttonColors(
                        containerColor = getDynamicThemeColor(0, appTheme, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary).first,
                        contentColor = getDynamicThemeColor(0, appTheme, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary).second
                    ),
                    onClick = {
                        scope.launch {"""
content = content.replace(target_btn1, replacement_btn1)

# Por Foto
target_btn2 = """                Button(
                    onClick = {
                        launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                    }
                ) {"""
replacement_btn2 = """                Button(
                    colors = ButtonDefaults.buttonColors(
                        containerColor = getDynamicThemeColor(1, appTheme, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary).first,
                        contentColor = getDynamicThemeColor(1, appTheme, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary).second
                    ),
                    onClick = {
                        launcher.launch(androidx.activity.result.PickVisualMediaRequest(ActivityResultContracts.PickVisualMedia.ImageOnly))
                    }
                ) {"""
content = content.replace(target_btn2, replacement_btn2)

# Manualmente
target_btn3 = """                Button(
                    onClick = {
                        selectedImageUri = null"""
replacement_btn3 = """                Button(
                    colors = ButtonDefaults.buttonColors(
                        containerColor = getDynamicThemeColor(2, appTheme, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary).first,
                        contentColor = getDynamicThemeColor(2, appTheme, MaterialTheme.colorScheme.primary, MaterialTheme.colorScheme.onPrimary).second
                    ),
                    onClick = {
                        selectedImageUri = null"""
content = content.replace(target_btn3, replacement_btn3)

with open("app/src/main/java/com/example/ui/AdminScreen.kt", "w") as f:
    f.write(content)
print("Success")
