sed -i '/val coroutineScope = rememberCoroutineScope()/i \            val isSyncing by viewModel.isSyncing.collectAsStateWithLifecycle()' app/src/main/java/com/example/ui/MestreScreen.kt

sed -i '/OutlinedCard(/i \
            Button(\
                onClick = { viewModel.syncDatabase() },\
                modifier = Modifier.fillMaxWidth(),\
                enabled = !isSyncing\
            ) {\
                if (isSyncing) {\
                    androidx.compose.material3.CircularProgressIndicator(\
                        modifier = Modifier.size(24.dp), \
                        color = MaterialTheme.colorScheme.onPrimary\
                    )\
                    Spacer(modifier = Modifier.width(8.dp))\
                    Text("Sincronizando...")\
                } else {\
                    Icon(androidx.compose.material.icons.Icons.Default.Sync, contentDescription = null)\
                    Spacer(modifier = Modifier.width(8.dp))\
                    Text("Sincronizar Banco de Dados")\
                }\
            }\
            Spacer(modifier = Modifier.height(16.dp))\
' app/src/main/java/com/example/ui/MestreScreen.kt
