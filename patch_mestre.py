import re

with open('app/src/main/java/com/example/ui/MestreScreen.kt', 'r') as f:
    content = f.read()

content = content.replace('com.example.data.FirebaseService.uploadBanner(context, selectedUri!!)', 'com.example.data.FirebaseService.uploadBanner(selectedUri!!)')

with open('app/src/main/java/com/example/ui/MestreScreen.kt', 'w') as f:
    f.write(content)
print("Patched MestreScreen")
