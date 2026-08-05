sed -i 's/fun addProduct(name: String, code: String, category: String, unit: String)/fun addProduct(name: String, code: String, category: String, unit: String, imageUrl: String? = null)/g' app/src/main/java/com/example/ui/MainViewModel.kt
sed -i 's/unit = unit/unit = unit,\n                imageUrl = imageUrl/g' app/src/main/java/com/example/ui/MainViewModel.kt
