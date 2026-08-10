import re
content = open("app/build.gradle.kts").read()
if "implementation(libs.firebase.messaging)" not in content:
    content = content.replace('implementation(libs.firebase.firestore)', 'implementation(libs.firebase.firestore)\n    implementation(libs.firebase.messaging)')
    open("app/build.gradle.kts", "w").write(content)
