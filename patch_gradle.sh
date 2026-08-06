sed -i 's|storeFile = file("${rootDir}/debug.keystore")|storeFile = file("${projectDir}/keystore.jks")|g' app/build.gradle.kts
sed -i 's|keyAlias = "androiddebugkey"|keyAlias = "app-key"|g' app/build.gradle.kts
