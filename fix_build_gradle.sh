# Remove the second dependencies block
sed -i '/dependencies {/,$d' app/build.gradle.kts
# Add the dependencies back to the main block
sed -i '/"ksp"(libs.moshi.kotlin.codegen)/a \  implementation("com.google.mlkit:barcode-scanning:17.2.0")\n  implementation("com.google.guava:guava:31.1-android")' app/build.gradle.kts
