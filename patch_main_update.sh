sed -i '/setContent {/a \
            var updateInfo by remember { mutableStateOf<com.example.util.GitHubUpdater.UpdateInfo?>(null) }\
            var showUpdateDialog by remember { mutableStateOf(false) }\
            LaunchedEffect(Unit) {\
                val info = com.example.util.GitHubUpdater.checkForUpdate()\
                if (info.isUpdateAvailable && info.downloadUrl != null) {\
                    updateInfo = info\
                    showUpdateDialog = true\
                }\
            }\
            if (showUpdateDialog && updateInfo != null) {\
                AlertDialog(\
                    onDismissRequest = { showUpdateDialog = false },\
                    title = { Text("Nova Atualização Disponível") },\
                    text = { Text("Uma nova versão (${updateInfo!!.latestVersion}) do aplicativo está disponível. Deseja atualizar agora?") },\
                    confirmButton = {\
                        TextButton(onClick = {\
                            showUpdateDialog = false\
                            com.example.util.GitHubUpdater.downloadAndInstallUpdate(this@MainActivity, updateInfo!!.downloadUrl!!)\
                        }) {\
                            Text("Atualizar")\
                        }\
                    },\
                    dismissButton = {\
                        TextButton(onClick = { showUpdateDialog = false }) {\
                            Text("Mais tarde")\
                        }\
                    }\
                )\
            }\
' app/src/main/java/com/example/MainActivity.kt
