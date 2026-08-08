import re

with open('app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    content = f.read()

# Make updateProduct upload image and save to Firebase
pattern_update = re.compile(r'fun updateProduct\(product: Product\) \{\s*viewModelScope\.launch \{\s*repository\.updateProduct\(product\)\s*\}\s*\}')
replacement_update = '''fun updateProduct(product: Product) {
        viewModelScope.launch {
            var finalProduct = product
            if (product.imageUrl?.startsWith("content://") == true) {
                val uri = android.net.Uri.parse(product.imageUrl)
                val url = com.example.data.FirebaseService.uploadImageToStorage(uri, "products/${product.code}_${System.currentTimeMillis()}.jpg")
                if (url != null) {
                    finalProduct = product.copy(imageUrl = url)
                }
            }
            repository.updateProduct(finalProduct)
            if (com.example.data.FirebaseService.isFirebaseConfigured()) {
                com.example.data.FirebaseService.saveProduct(finalProduct)
                _syncMessage.emit("Produto atualizado na nuvem!")
            }
        }
    }
'''

content = pattern_update.sub(replacement_update, content)

# Make addProduct upload image and save to Firebase
pattern_add = re.compile(r'fun addProduct\(name: String, code: String, category: String, unit: String, imageUrl: String\? = null\) \{[\s\S]*?_newProductsCount\.value \+= 1\s*\}\s*\}')
replacement_add = '''fun addProduct(name: String, code: String, category: String, unit: String, imageUrl: String? = null) {
        viewModelScope.launch {
            var finalImageUrl = imageUrl
            if (imageUrl?.startsWith("content://") == true) {
                val uri = android.net.Uri.parse(imageUrl)
                val url = com.example.data.FirebaseService.uploadImageToStorage(uri, "products/${code}_${System.currentTimeMillis()}.jpg")
                if (url != null) {
                    finalImageUrl = url
                }
            }
            val product = Product(
                code = code,
                name = name,
                searchName = name.lowercase().replace(Regex("[áàâã]"), "a").replace(Regex("[éèê]"), "e").replace(Regex("[íìî]"), "i").replace(Regex("[óòôõ]"), "o").replace(Regex("[úùû]"), "u").replace(Regex("[ç]"), "c"),
                category = category,
                unit = unit,
                imageUrl = finalImageUrl
            )
            repository.insertProduct(product)
            if (!com.example.data.FirebaseService.isFirebaseConfigured()) {
                _syncMessage.emit("Salvo apenas localmente (Nuvem não configurada)")
            } else {
                com.example.data.FirebaseService.saveProduct(product)
                _syncMessage.emit("Produto adicionado na nuvem!")
            }
            _newProductsCount.value += 1
        }
    }'''

content = pattern_add.sub(replacement_add, content)

# Add deleteProduct
pattern_delete_tab = re.compile(r'fun deleteTab\(tab: com\.example\.data\.DynamicTab\) = viewModelScope\.launch \{')
replacement_delete_tab = '''fun deleteProduct(product: Product) {
        viewModelScope.launch {
            repository.deleteProduct(product)
            if (com.example.data.FirebaseService.isFirebaseConfigured()) {
                com.example.data.FirebaseService.deleteProduct(product.code)
                _syncMessage.emit("Produto excluído na nuvem!")
            }
        }
    }

    fun deleteTab(tab: com.example.data.DynamicTab) = viewModelScope.launch {'''

content = pattern_delete_tab.sub(replacement_delete_tab, content)

with open('app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(content)
print("Patched MainViewModel (update/add/delete)")
