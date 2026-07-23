cat app/src/main/java/com/example/ui/MestreScreen.kt | awk '
/val context = androidx.compose.ui.platform.LocalContext.current/ {
    print "            var showConfirmDialog by remember { mutableStateOf(false) }"
    print "            var selectedUri by remember { mutableStateOf<android.net.Uri?>(null) }"
    print $0
    next
}
/val launcher = androidx.activity.compose.rememberLauncherForActivityResult/ {
    print "            val launcher = androidx.activity.compose.rememberLauncherForActivityResult("
    print "                contract = androidx.activity.result.contract.ActivityResultContracts.GetContent()"
    print "            ) { uri: android.net.Uri? ->"
    print "                uri?.let {"
    print "                    selectedUri = it"
    print "                    showConfirmDialog = true"
    print "                }"
    print "            }"
    print "            if (showConfirmDialog && selectedUri != null) {"
    print "                AlertDialog("
    print "                    onDismissRequest = { showConfirmDialog = false },"
    print "                    title = { Text(\"Alterar Fundo\") },"
    print "                    text = { Text(\"Tem certeza que deseja alterar a imagem de fundo de todos os usuários?\") },"
    print "                    confirmButton = {"
    print "                        TextButton(onClick = {"
    print "                            showConfirmDialog = false"
    print "                            coroutineScope.launch {"
    print "                                try {"
    print "                                    val inputStream = context.contentResolver.openInputStream(selectedUri!!)"
    print "                                    val file = java.io.File(context.filesDir, \"custom_hero_banner.jpg\")"
    print "                                    val outputStream = java.io.FileOutputStream(file)"
    print "                                    inputStream?.copyTo(outputStream)"
    print "                                    inputStream?.close()"
    print "                                    outputStream.close()"
    print "                                    viewModel.userPreferences.setBannerImageUri(file.absolutePath)"
    print "                                    android.widget.Toast.makeText(context, \"Fundo alterado com sucesso!\", android.widget.Toast.LENGTH_SHORT).show()"
    print "                                } catch (e: Exception) {"
    print "                                    android.widget.Toast.makeText(context, \"Erro ao salvar imagem\", android.widget.Toast.LENGTH_SHORT).show()"
    print "                                }"
    print "                            }"
    print "                        }) {"
    print "                            Text(\"Confirmar\")"
    print "                        }"
    print "                    },"
    print "                    dismissButton = {"
    print "                        TextButton(onClick = { showConfirmDialog = false }) {"
    print "                            Text(\"Cancelar\")"
    print "                        }"
    print "                    }"
    print "                )"
    print "            }"
    skip = 1
    next
}
skip && /OutlinedCard\(/ {
    skip = 0
}
skip { next }
{ print $0 }
' > MestreScreen_new.kt
mv MestreScreen_new.kt app/src/main/java/com/example/ui/MestreScreen.kt
