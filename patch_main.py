import re
content = open("app/src/main/java/com/example/MainActivity.kt").read()

imports = """import com.google.firebase.messaging.FirebaseMessaging
import com.example.util.NotificationHelper
"""
content = content.replace("import com.example.util.NotificationHelper", imports)

sub_code = """
        super.onCreate(savedInstanceState)
        
        try {
            FirebaseMessaging.getInstance().subscribeToTopic("products")
                .addOnCompleteListener { task ->
                    if (!task.isSuccessful) {
                        android.util.Log.e("FCM", "Failed to subscribe to topic")
                    }
                }
        } catch(e: Exception) {
            android.util.Log.e("FCM", "Firebase not configured")
        }
"""
content = content.replace("        super.onCreate(savedInstanceState)", sub_code)
open("app/src/main/java/com/example/MainActivity.kt", "w").write(content)
