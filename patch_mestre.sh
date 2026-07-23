sed -i '/HorizontalDivider()/i \
            Spacer(modifier = Modifier.height(16.dp))\
            val context = androidx.compose.ui.platform.LocalContext.current\
            val coroutineScope = rememberCoroutineScope()\
            val launcher = androidx.activity.compose.rememberLauncherForActivityResult(\
                contract = androidx.activity.result.contract.ActivityResultContracts.GetContent()\
            ) { uri: android.net.Uri? ->\
                uri?.let {\
                    coroutineScope.launch {\
                        try {\
                            val inputStream = context.contentResolver.openInputStream(uri)\
                            val file = java.io.File(context.filesDir, "custom_hero_banner.jpg")\
                            val outputStream = java.io.FileOutputStream(file)\
                            inputStream?.copyTo(outputStream)\
                            inputStream?.close()\
                            outputStream.close()\
                            viewModel.userPreferences.setBannerImageUri(file.absolutePath)\
                            android.widget.Toast.makeText(context, "Fundo alterado com sucesso!", android.widget.Toast.LENGTH_SHORT).show()\
                        } catch (e: Exception) {\
                            android.widget.Toast.makeText(context, "Erro ao salvar imagem", android.widget.Toast.LENGTH_SHORT).show()\
                        }\
                    }\
                }\
            }\
            OutlinedCard(\
                modifier = Modifier.fillMaxWidth(),\
                onClick = { launcher.launch("image/*") }\
            ) {\
                Row(\
                    modifier = Modifier.padding(16.dp),\
                    verticalAlignment = Alignment.CenterVertically\
                ) {\
                    Icon(Icons.Default.ColorLens, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))\
                    Spacer(modifier = Modifier.width(16.dp))\
                    Column {\
                        Text("Alterar Fundo do App (Hero Banner)", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)\
                        Text("Escolha uma imagem da galeria.", style = MaterialTheme.typography.bodySmall)\
                    }\
                }\
            }' app/src/main/java/com/example/ui/MestreScreen.kt
