import re

with open("app/src/main/AndroidManifest.xml", "r") as f:
    content = f.read()

if "android.permission.VIBRATE" not in content:
    content = content.replace('<uses-permission android:name="android.permission.INTERNET" />', '<uses-permission android:name="android.permission.INTERNET" />\n    <uses-permission android:name="android.permission.VIBRATE" />')

with open("app/src/main/AndroidManifest.xml", "w") as f:
    f.write(content)
