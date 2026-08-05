sed -i '284,286d' app/src/main/java/com/example/ui/MainViewModel.kt
sed -i '283a \
    fun clearNewProductsCount() {\
        _newProductsCount.value = 0\
    }' app/src/main/java/com/example/ui/MainViewModel.kt
