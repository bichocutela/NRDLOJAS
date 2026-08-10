package com.example.util

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.ActivityCompat
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.example.R

import android.widget.Toast

object NotificationHelper {
    private const val CHANNEL_ID = "new_products_channel"
    private const val NOTIFICATION_ID = 1001

    private var currentToast: Toast? = null

    fun showToast(context: Context, message: String, length: Int = Toast.LENGTH_SHORT) {
        currentToast?.cancel()
        currentToast = Toast.makeText(context, message, length)
        currentToast?.show()
    }

    fun createNotificationChannel(context: Context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val name = "Novos Produtos"
            val descriptionText = "Notificações quando novos produtos são adicionados"
            val importance = NotificationManager.IMPORTANCE_DEFAULT
            val channel = NotificationChannel(CHANNEL_ID, name, importance).apply {
                description = descriptionText
            }
            val notificationManager: NotificationManager =
                context.getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
            notificationManager.createNotificationChannel(channel)
        }
    }

    fun showProductEventNotification(context: Context, type: String, productName: String, oldName: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ActivityCompat.checkSelfPermission(
                    context,
                    android.Manifest.permission.POST_NOTIFICATIONS
                ) != PackageManager.PERMISSION_GRANTED
            ) {
                return
            }
        }

        val title = if (type == "NEW_PRODUCT") "Novo produto adicionado" else "Produto atualizado"
        val text = when (type) {
            "NEW_PRODUCT" -> "$productName foi adicionado ao aplicativo."
            "CODE_CHANGED" -> "O código de $productName foi atualizado."
            "NAME_CHANGED" -> "$oldName agora aparece como $productName."
            "INFO_CHANGED" -> "As informações de $productName foram atualizadas."
            else -> "$productName foi atualizado."
        }

        val builder = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_dialog_info)
            .setContentTitle(title)
            .setContentText(text)
            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)

        with(NotificationManagerCompat.from(context)) {
            notify(System.currentTimeMillis().toInt(), builder.build())
        }
    }
}
