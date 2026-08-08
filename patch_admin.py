import re

with open('app/src/main/java/com/example/ui/AdminScreen.kt', 'r') as f:
    content = f.read()

# Replace the explicit call with a comment
new_content = content.replace(
    'com.example.util.NotificationHelper.showNewProductNotification(context, productName)',
    '// com.example.util.NotificationHelper.showNewProductNotification(context, productName) // Deixando via Firebase para evitar duplicidade'
)

with open('app/src/main/java/com/example/ui/AdminScreen.kt', 'w') as f:
    f.write(new_content)
