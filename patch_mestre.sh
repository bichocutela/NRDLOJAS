sed -i '/Spacer(modifier = Modifier.height(16.dp))/a \
            OutlinedCard(\
                modifier = Modifier.fillMaxWidth(),\
                onClick = {\
                    coroutineScope.launch {\
                        val hasUpdate = com.example.util.GitHubUpdater.checkForUpdates(context, com.example.BuildConfig.VERSION_NAME)\
                        if (!hasUpdate) {\
                            com.example.util.NotificationHelper.showToast(context, "Você já possui a versão mais recente.", android.widget.Toast.LENGTH_SHORT)\
                        }\
                    }\
                }\
            ) {\
                Row(\
                    modifier = Modifier.padding(16.dp),\
                    verticalAlignment = Alignment.CenterVertically\
                ) {\
                    Icon(Icons.Default.Sync, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))\
                    Spacer(modifier = Modifier.width(16.dp))\
                    Column {\
                        Text("Sincronizar Atualização (GitHub)", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)\
                        Text("Verificar se há nova versão no GitHub.", style = MaterialTheme.typography.bodySmall)\
                    }\
                }\
            }\
            Spacer(modifier = Modifier.height(16.dp))' app/src/main/java/com/example/ui/MestreScreen.kt
