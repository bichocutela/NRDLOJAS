import sys

with open("app/src/main/java/com/example/ui/MestreScreen.kt", "r") as f:
    content = f.read()

target = """                                    if (url != null) {
                                        com.example.util.NotificationHelper.showToast(context, "Fundo alterado com sucesso para todos!", android.widget.Toast.LENGTH_SHORT)
                                        viewModel.userPreferences.setBannerImageUri(url)
                                    } else {
                                        val error = com.example.data.FirebaseService.lastError ?: "Firebase offline ou erro desconhecido"
                                        com.example.util.NotificationHelper.showToast(context, "Erro: $error", android.widget.Toast.LENGTH_LONG)
                                        // Fallback para local apenas
                                        val inputStream = context.contentResolver.openInputStream(selectedUri!!)
                                        val file = java.io.File(context.filesDir, "custom_hero_banner.jpg")
                                        val outputStream = java.io.FileOutputStream(file)
                                        inputStream?.copyTo(outputStream)
                                        inputStream?.close()
                                        outputStream.close()
                                        viewModel.userPreferences.setBannerImageUri(file.absolutePath)
                                        com.example.util.NotificationHelper.showToast(context, "Fundo alterado (apenas local)", android.widget.Toast.LENGTH_SHORT)
                                    }"""

replacement = """                                    if (url != null) {
                                        com.example.util.NotificationHelper.showToast(context, "Fundo alterado com sucesso para todos!", android.widget.Toast.LENGTH_SHORT)
                                    } else {
                                        val error = com.example.data.FirebaseService.lastError ?: "Firebase offline ou erro desconhecido"
                                        com.example.util.NotificationHelper.showToast(context, "Erro: $error", android.widget.Toast.LENGTH_LONG)
                                    }"""

if target in content:
    content = content.replace(target, replacement)
    with open("app/src/main/java/com/example/ui/MestreScreen.kt", "w") as f:
        f.write(content)
    print("Patched successfully.")
else:
    print("Target not found.")

