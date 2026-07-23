import re

with open("app/build.gradle.kts", "r") as f:
    content = f.read()

content = content.replace("implementation(platform(libs.firebase.bom))", "// implementation(platform(libs.firebase.bom))")
content = content.replace("implementation(libs.firebase.ai)", "// implementation(libs.firebase.ai)")
content = content.replace("implementation(libs.firebase.appcheck.recaptcha)", "// implementation(libs.firebase.appcheck.recaptcha)")
content = content.replace("googleServices { missingGoogleServicesStrategy = MissingGoogleServicesStrategy.WARN }", "// googleServices { missingGoogleServicesStrategy = MissingGoogleServicesStrategy.WARN }")
content = content.replace("alias(libs.plugins.google.services)", "// alias(libs.plugins.google.services)")

with open("app/build.gradle.kts", "w") as f:
    f.write(content)
