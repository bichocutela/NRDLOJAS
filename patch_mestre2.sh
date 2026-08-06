awk '
{
    print
    if ($0 ~ /Adicionar usando Gemini ou manualmente/) {
        print "                    }"
        print "                }"
        print "            }"
        print ""
        print "            Spacer(modifier = Modifier.height(16.dp))"
        print "            OutlinedCard("
        print "                modifier = Modifier.fillMaxWidth(),"
        print "                onClick = {"
        print "                    coroutineScope.launch {"
        print "                        val hasUpdate = com.example.util.GitHubUpdater.checkForUpdates(context, com.example.BuildConfig.VERSION_NAME)"
        print "                        if (!hasUpdate) {"
        print "                            com.example.util.NotificationHelper.showToast(context, \"Você já possui a versão mais recente.\", android.widget.Toast.LENGTH_SHORT)"
        print "                        }"
        print "                    }"
        print "                }"
        print "            ) {"
        print "                Row("
        print "                    modifier = Modifier.padding(16.dp),"
        print "                    verticalAlignment = Alignment.CenterVertically"
        print "                ) {"
        print "                    Icon(Icons.Default.CloudDownload, contentDescription = null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(32.dp))"
        print "                    Spacer(modifier = Modifier.width(16.dp))"
        print "                    Column {"
        print "                        Text(\"Sincronizar Atualização (GitHub)\", fontWeight = androidx.compose.ui.text.font.FontWeight.Bold)"
        print "                        Text(\"Baixar e instalar nova versão do app.\", style = MaterialTheme.typography.bodySmall)"
        print "                    }"
        print "                }"
        print "            }"
        # Skip the next 3 lines because we printed them above
        getline
        getline
        getline
    }
}' app/src/main/java/com/example/ui/MestreScreen.kt > app/src/main/java/com/example/ui/MestreScreen.kt.new
mv app/src/main/java/com/example/ui/MestreScreen.kt.new app/src/main/java/com/example/ui/MestreScreen.kt
