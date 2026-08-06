package com.example.util

import android.app.DownloadManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.util.Log
import androidx.core.content.FileProvider
import com.example.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.net.HttpURLConnection
import java.net.URL

object GitHubUpdater {
    private const val REPO = "bichocutela/NRDLOJAS"
    private const val API_URL = "https://api.github.com/repos/$REPO/releases/latest"

    data class UpdateInfo(
        val isUpdateAvailable: Boolean,
        val latestVersion: String,
        val downloadUrl: String?
    )

    suspend fun checkForUpdate(): UpdateInfo = withContext(Dispatchers.IO) {
        try {
            val url = URL(API_URL)
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "GET"
            connection.setRequestProperty("Accept", "application/vnd.github.v3+json")
            
            if (connection.responseCode == HttpURLConnection.HTTP_OK) {
                val response = connection.inputStream.bufferedReader().use { it.readText() }
                val json = JSONObject(response)
                
                val tagName = json.getString("tag_name").replace("v", "") // e.g. "1.0.15"
                val currentVersion = BuildConfig.VERSION_NAME // e.g. "1.0.1"
                
                val currentRunNumber = currentVersion.split(".").lastOrNull()?.toIntOrNull() ?: 0
                val latestRunNumber = tagName.split(".").lastOrNull()?.toIntOrNull() ?: 0
                
                var downloadUrl: String? = null
                if (json.has("assets")) {
                    val assets = json.getJSONArray("assets")
                    if (assets.length() > 0) {
                        downloadUrl = assets.getJSONObject(0).getString("browser_download_url")
                    }
                }
                
                return@withContext UpdateInfo(
                    isUpdateAvailable = latestRunNumber > currentRunNumber,
                    latestVersion = tagName,
                    downloadUrl = downloadUrl
                )
            }
        } catch (e: Exception) {
            Log.e("GitHubUpdater", "Error checking for update", e)
        }
        return@withContext UpdateInfo(false, BuildConfig.VERSION_NAME, null)
    }

    fun downloadAndInstallUpdate(context: Context, downloadUrl: String) {
        val fileName = "update_app.apk"
        val destination = File(context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), fileName)
        if (destination.exists()) destination.delete()

        val request = DownloadManager.Request(Uri.parse(downloadUrl))
            .setTitle("Atualizando Aplicativo")
            .setDescription("Baixando a versão mais recente...")
            .setDestinationUri(Uri.fromFile(destination))
            .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
            .setAllowedOverMetered(true)
            .setAllowedOverRoaming(true)

        val downloadManager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
        val downloadId = downloadManager.enqueue(request)

        val onComplete = object : BroadcastReceiver() {
            override fun onReceive(ctxt: Context, intent: Intent) {
                val id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1)
                if (id == downloadId) {
                    installApk(context, destination)
                    context.unregisterReceiver(this)
                }
            }
        }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            context.registerReceiver(onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE), Context.RECEIVER_EXPORTED)
        } else {
            context.registerReceiver(onComplete, IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE))
        }
        
        NotificationHelper.showToast(context, "Baixando atualização...", android.widget.Toast.LENGTH_SHORT)
    }

    private fun installApk(context: Context, apkFile: File) {
        try {
            val apkUri = FileProvider.getUriForFile(
                context,
                "${context.packageName}.fileprovider",
                apkFile
            )
            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(apkUri, "application/vnd.android.package-archive")
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
            }
            context.startActivity(intent)
        } catch (e: Exception) {
            Log.e("GitHubUpdater", "Error installing APK", e)
            NotificationHelper.showToast(context, "Erro ao instalar a atualização.", android.widget.Toast.LENGTH_LONG)
        }
    }
}
