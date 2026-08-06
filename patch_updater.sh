cat << 'INNER_EOF' > app/src/main/java/com/example/util/GitHubUpdater.kt.new
package com.example.util

import android.app.DownloadManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.Build
import android.os.Environment
import androidx.core.content.FileProvider
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL
import androidx.core.content.ContextCompat

object GitHubUpdater {
    private const val REPO_OWNER = "bichocutela"
    private const val REPO_NAME = "NRDLOJAS"
    private const val API_URL = "https://api.github.com/repos/\$REPO_OWNER/\$REPO_NAME/releases/latest"

    suspend fun checkForUpdates(context: Context, currentVersionName: String): Boolean = withContext(Dispatchers.IO) {
        try {
            val url = URL(API_URL)
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "GET"
            connection.setRequestProperty("Accept", "application/vnd.github.v3+json")

            if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                val response = connection.inputStream.bufferedReader().use { it.readText() }
                val jsonResponse = JSONObject(response)
                val latestVersion = jsonResponse.getString("tag_name").removePrefix("v")
                
                if (isNewerVersion(currentVersionName, latestVersion)) {
                    val assets = jsonResponse.getJSONArray("assets")
                    if (assets.length() > 0) {
                        val apkUrl = assets.getJSONObject(0).getString("browser_download_url")
                        withContext(Dispatchers.Main) {
                            downloadAndInstallApk(context, apkUrl, latestVersion)
                        }
                        return@withContext true
                    }
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext false
    }

    private fun isNewerVersion(current: String, latest: String): Boolean {
        val currentParts = current.split(".").mapNotNull { it.toIntOrNull() }
        val latestParts = latest.split(".").mapNotNull { it.toIntOrNull() }

        for (i in 0 until maxOf(currentParts.size, latestParts.size)) {
            val curr = currentParts.getOrElse(i) { 0 }
            val lat = latestParts.getOrElse(i) { 0 }
            if (lat > curr) return true
            if (lat < curr) return false
        }
        return false
    }

    private fun downloadAndInstallApk(context: Context, apkUrl: String, version: String) {
        val destination = context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
        val apkFile = File(destination, "app-update-\$version.apk")
        
        if (apkFile.exists()) {
            apkFile.delete()
        }

        val request = DownloadManager.Request(Uri.parse(apkUrl))
            .setTitle("Atualização do Aplicativo")
            .setDescription("Baixando nova versão...")
            .setDestinationUri(Uri.fromFile(apkFile))
            .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
            .setAllowedOverMetered(true)
            .setAllowedOverRoaming(true)

        val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
        val downloadId = downloadManager.enqueue(request)

        val onComplete = object : BroadcastReceiver() {
            override fun onReceive(ctxt: Context, intent: Intent) {
                if (intent.action == DownloadManager.ACTION_DOWNLOAD_COMPLETE) {
                    val id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1)
                    if (id == downloadId) {
                        context.unregisterReceiver(this)
                        installApk(context, apkFile)
                    }
                }
            }
        }
        
        ContextCompat.registerReceiver(context, onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE), ContextCompat.RECEIVER_EXPORTED)

        NotificationHelper.showToast(context, "Baixando atualização...", android.widget.Toast.LENGTH_SHORT)
    }

    private fun installApk(context: Context, apkFile: File) {
        try {
            val apkUri = FileProvider.getUriForFile(
                context,
                "\${context.packageName}.fileprovider",
                apkFile
            )

            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(apkUri, "application/vnd.android.package-archive")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
            }
            context.startActivity(intent)
        } catch (e: Exception) {
            e.printStackTrace()
            NotificationHelper.showToast(context, "Erro ao instalar atualização.", android.widget.Toast.LENGTH_LONG)
        }
    }
}
INNER_EOF
mv app/src/main/java/com/example/util/GitHubUpdater.kt.new app/src/main/java/com/example/util/GitHubUpdater.kt
