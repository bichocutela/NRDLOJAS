sed -i 's|storeFile = file("${projectDir}/keystore.jks")|storeFile = file("${rootDir}/debug.keystore")|g' app/build.gradle.kts
sed -i 's|keyAlias = "app-key"|keyAlias = "androiddebugkey"|g' app/build.gradle.kts
