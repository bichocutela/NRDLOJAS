# Fix AdminScreen.kt getBitmap
sed -i 's/MediaStore.Images.Media.getBitmap(context.contentResolver, it)/if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.P) android.graphics.ImageDecoder.decodeBitmap(android.graphics.ImageDecoder.createSource(context.contentResolver, it)) else MediaStore.Images.Media.getBitmap(context.contentResolver, it)/g' app/src/main/java/com/example/ui/AdminScreen.kt

# Fix MainViewModel.kt OptIns
sed -i 's/import kotlinx.coroutines.flow.debounce/import kotlinx.coroutines.FlowPreview\nimport kotlinx.coroutines.ExperimentalCoroutinesApi\nimport kotlinx.coroutines.flow.debounce/g' app/src/main/java/com/example/ui/MainViewModel.kt
sed -i 's/@OptIn(kotlinx.coroutines.FlowPreview::class)//g' app/src/main/java/com/example/ui/MainViewModel.kt
sed -i 's/@OptIn(kotlinx.coroutines.ExperimentalCoroutinesApi::class)//g' app/src/main/java/com/example/ui/MainViewModel.kt
sed -i 's/class MainViewModel/@OptIn(FlowPreview::class, ExperimentalCoroutinesApi::class)\nclass MainViewModel/g' app/src/main/java/com/example/ui/MainViewModel.kt

