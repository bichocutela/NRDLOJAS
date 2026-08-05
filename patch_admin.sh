sed -i '75a \
    val isSyncing by viewModel.isSyncing.collectAsStateWithLifecycle()' app/src/main/java/com/example/ui/AdminScreen.kt

sed -i '/Text("Exportar Inventário (PDF)")/ {
    N
    N
    a \
                Spacer(modifier = Modifier.height(16.dp))\
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
                        Icon(Icons.Default.Sync, contentDescription = null)\
                        Spacer(modifier = Modifier.width(8.dp))\
                        Text("Sincronizar Banco de Dados")\
                    }\
                }
}' app/src/main/java/com/example/ui/AdminScreen.kt
