import sys

with open("app/src/main/java/com/example/ui/AboutScreen.kt", "r") as f:
    content = f.read()

target1 = """            var updateTag by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
            var updateUrl by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }"""

replacement1 = """            var updateTag by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
            var updateUrl by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }

            var isGeneratingQr by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
            var showQrDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
            var showQrErrorDialog by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf(false) }
            var qrTag by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }
            var qrUrl by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf("") }"""

content = content.replace(target1, replacement1)

target2 = """                } else {
                    Text("Verificar Atualizações")
                }
            }
        }
    }
}"""

replacement2 = """                } else {
                    Text("Verificar Atualizações")
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            Button(
                onClick = {
                    isGeneratingQr = true
                    coroutineScope.launch {
                        val release = com.example.util.UpdateChecker.checkLatestRelease()
                        isGeneratingQr = false
                        if (release != null && release.second.startsWith("http")) {
                            qrTag = release.first
                            if (!qrTag.startsWith("v")) qrTag = "v$qrTag"
                            qrUrl = release.second
                            showQrDialog = true
                        } else {
                            showQrErrorDialog = true
                        }
                    }
                },
                modifier = Modifier.fillMaxWidth(),
                enabled = !isGeneratingQr
            ) {
                if (isGeneratingQr) {
                    CircularProgressIndicator(
                        modifier = Modifier.size(24.dp),
                        color = MaterialTheme.colorScheme.onPrimary,
                        strokeWidth = 2.dp
                    )
                } else {
                    Text("Gerar versão em QR Code")
                }
            }

            if (showQrErrorDialog) {
                AlertDialog(
                    onDismissRequest = { showQrErrorDialog = false },
                    title = { Text("Não foi possível gerar o QR Code no momento.") },
                    text = { Text("Verifique sua conexão e tente novamente.") },
                    confirmButton = {
                        TextButton(onClick = {
                            showQrErrorDialog = false
                            isGeneratingQr = true
                            coroutineScope.launch {
                                val release = com.example.util.UpdateChecker.checkLatestRelease()
                                isGeneratingQr = false
                                if (release != null && release.second.startsWith("http")) {
                                    qrTag = release.first
                                    if (!qrTag.startsWith("v")) qrTag = "v$qrTag"
                                    qrUrl = release.second
                                    showQrDialog = true
                                } else {
                                    showQrErrorDialog = true
                                }
                            }
                        }) {
                            Text("Tentar novamente")
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showQrErrorDialog = false }) {
                            Text("Fechar")
                        }
                    }
                )
            }

            if (showQrDialog) {
                AlertDialog(
                    onDismissRequest = { showQrDialog = false },
                    title = {
                        Text(
                            text = "Compartilhar NRD Códigos",
                            textAlign = androidx.compose.ui.text.style.TextAlign.Center,
                            modifier = Modifier.fillMaxWidth()
                        )
                    },
                    text = {
                        Column(
                            horizontalAlignment = Alignment.CenterHorizontally,
                            modifier = Modifier.fillMaxWidth()
                        ) {
                            Text("Versão disponível: $qrTag")
                            Spacer(modifier = Modifier.height(16.dp))

                            val bitmap = androidx.compose.runtime.remember(qrUrl) {
                                generateQrCodeBitmap(qrUrl)
                            }

                            if (bitmap != null) {
                                androidx.compose.foundation.Image(
                                    bitmap = androidx.compose.ui.graphics.asImageBitmap(bitmap),
                                    contentDescription = "QR Code",
                                    modifier = Modifier.size(200.dp),
                                    contentScale = androidx.compose.ui.layout.ContentScale.Fit
                                )
                            } else {
                                Text("Erro ao gerar a imagem do QR Code.", color = MaterialTheme.colorScheme.error)
                            }

                            Spacer(modifier = Modifier.height(16.dp))
                            Text("Escaneie para baixar esta versão", style = MaterialTheme.typography.bodySmall)
                        }
                    },
                    confirmButton = {
                        TextButton(onClick = {
                            val clipboard = context.getSystemService(android.content.Context.CLIPBOARD_SERVICE) as android.content.ClipboardManager
                            val clip = android.content.ClipData.newPlainText("URL", qrUrl)
                            clipboard.setPrimaryClip(clip)
                            android.widget.Toast.makeText(context, "Link copiado!", android.widget.Toast.LENGTH_SHORT).show()
                        }) {
                            Text("Copiar link")
                        }
                    },
                    dismissButton = {
                        TextButton(onClick = { showQrDialog = false }) {
                            Text("Fechar")
                        }
                    }
                )
            }
        }
    }
}

fun generateQrCodeBitmap(content: String, size: Int = 512): android.graphics.Bitmap? {
    try {
        val bitMatrix = com.google.zxing.MultiFormatWriter().encode(
            content,
            com.google.zxing.BarcodeFormat.QR_CODE,
            size,
            size
        )
        val width = bitMatrix.width
        val height = bitMatrix.height
        val bitmap = android.graphics.Bitmap.createBitmap(width, height, android.graphics.Bitmap.Config.ARGB_8888)
        
        for (x in 0 until width) {
            for (y in 0 until height) {
                bitmap.setPixel(x, y, if (bitMatrix.get(x, y)) android.graphics.Color.BLACK else android.graphics.Color.WHITE)
            }
        }
        return bitmap
    } catch (e: Exception) {
        e.printStackTrace()
        return null
    }
}"""

content = content.replace(target2, replacement2)

with open("app/src/main/java/com/example/ui/AboutScreen.kt", "w") as f:
    f.write(content)
