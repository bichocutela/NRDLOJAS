sed -i '118a \
            var bannerUrlInput by remember { mutableStateOf("") }\
            var showUrlDialog by remember { mutableStateOf(false) }' app/src/main/java/com/example/ui/MestreScreen.kt

sed -i '/HorizontalDivider()/i \
            Spacer(modifier = Modifier.height(16.dp))\
            OutlinedCard(\
                modifier = Modifier.fillMaxWidth(),\
                onClick = { showUrlDialog = true }\
            ) {\
                Row(\
                    modifier = Modifier.padding(16.dp),\
                    verticalAlignment = Alignment.CenterVertically\
                ) {\
                    Icon(Icons.Default.ColorLens, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))\
                    Spacer(modifier = Modifier.width(16.dp))\
                    Column {\
                        Text("Alterar Fundo por URL", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)\
                        Text("Forneça um link (ex: Google Drive).", style = MaterialTheme.typography.bodySmall)\
                    }\
                }\
            }\
            \
            if (showUrlDialog) {\
                AlertDialog(\
                    onDismissRequest = { showUrlDialog = false },\
                    title = { Text("URL da Imagem") },\
                    text = {\
                        OutlinedTextField(\
                            value = bannerUrlInput,\
                            onValueChange = { bannerUrlInput = it },\
                            label = { Text("Cole o link aqui") },\
                            modifier = Modifier.fillMaxWidth()\
                        )\
                    },\
                    confirmButton = {\
                        TextButton(onClick = {\
                            showUrlDialog = false\
                            if (bannerUrlInput.isNotBlank()) {\
                                coroutineScope.launch {\
                                    try {\
                                        val url = com.example.data.FirebaseService.setBannerUrlDirectly(bannerUrlInput)\
                                        viewModel.userPreferences.setBannerImageUri(url)\
                                        com.example.util.NotificationHelper.showToast(context, "Fundo alterado com sucesso para todos!", android.widget.Toast.LENGTH_SHORT)\
                                    } catch (e: Exception) {\
                                        com.example.util.NotificationHelper.showToast(context, "Erro: ${e.message}", android.widget.Toast.LENGTH_LONG)\
                                    }\
                                }\
                            }\
                        }) {\
                            Text("Salvar")\
                        }\
                    },\
                    dismissButton = {\
                        TextButton(onClick = { showUrlDialog = false }) {\
                            Text("Cancelar")\
                        }\
                    }\
                )\
            }\
' app/src/main/java/com/example/ui/MestreScreen.kt
