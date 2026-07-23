sed -i 's/\/\/ alias(libs.plugins.google.services)/alias(libs.plugins.google.services)/g' app/build.gradle.kts
sed -i 's/\/\/ implementation(platform(libs.firebase.bom))/implementation(platform(libs.firebase.bom))/g' app/build.gradle.kts
sed -i 's/\/\/ implementation(libs.firebase.firestore)/implementation(libs.firebase.firestore)/g' app/build.gradle.kts
sed -i '/implementation(libs.firebase.firestore)/a \
    implementation(libs.firebase.storage)' app/build.gradle.kts
