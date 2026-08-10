import re

content = open("app/src/main/java/com/example/ui/MainViewModel.kt").read()

add_replacement = """    suspend fun addProductSuspend(name: String, code: String, category: String, unit: String, imageUrl: String? = null): Boolean {
        var finalImageUrl = imageUrl
        if (imageUrl?.startsWith("content://") == true) {
            android.util.Log.d("ProductSync", "Iniciando upload de imagem para $code")
            val uri = android.net.Uri.parse(imageUrl)
            val url = com.example.data.FirebaseService.uploadImageToStorage(uri, "products/${code}_${System.currentTimeMillis()}.jpg")
            if (url != null) {
                android.util.Log.d("ProductSync", "Upload sucesso: $url")
                finalImageUrl = url
            } else {
                android.util.Log.e("ProductSync", "Upload falhou para $code")
                _syncMessage.emit("Não foi possível enviar a foto. Tente novamente.")
                return false
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
        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            android.util.Log.d("ProductSync", "Iniciando save Firestore para novo produto: $code")
            val success = com.example.data.FirebaseService.saveProduct(product)
            if (success) {
                android.util.Log.d("ProductSync", "Save Firestore sucesso, atualizando Room: $code")
                repository.insertProduct(product)
                com.example.data.FirebaseService.publishProductEvent("NEW_PRODUCT", product.name, null, product.code)
                _syncMessage.emit("Produto adicionado na nuvem!")
                _newProductsCount.value += 1
                return true
            } else {
                android.util.Log.e("ProductSync", "Save Firestore falhou para: $code")
                _syncMessage.emit("Erro ao salvar produto na nuvem.")
                return false
            }
        } else {
            repository.insertProduct(product)
            _syncMessage.emit("Salvo apenas localmente (Nuvem não configurada)")
            _newProductsCount.value += 1
            return true
        }
    }"""

update_replacement = """    suspend fun updateProductSuspend(oldProduct: Product, newProduct: Product): Boolean {
        var finalProduct = newProduct
        finalProduct = finalProduct.copy(id = oldProduct.id)

        if (newProduct.imageUrl?.startsWith("content://") == true) {
            android.util.Log.d("ProductSync", "Iniciando upload de imagem para alteração: ${newProduct.code}")
            val uri = android.net.Uri.parse(newProduct.imageUrl)
            val url = com.example.data.FirebaseService.uploadImageToStorage(uri, "products/${newProduct.code}_${System.currentTimeMillis()}.jpg")
            if (url != null) {
                android.util.Log.d("ProductSync", "Upload sucesso: $url")
                finalProduct = finalProduct.copy(imageUrl = url)
            } else {
                android.util.Log.e("ProductSync", "Upload falhou para: ${newProduct.code}")
                _syncMessage.emit("Não foi possível enviar a foto. Tente novamente.")
                return false
            }
        }

        if (com.example.data.FirebaseService.isFirebaseConfigured()) {
            android.util.Log.d("ProductSync", "Iniciando save Firestore para edição: ${finalProduct.code}")
            val saveSuccess = com.example.data.FirebaseService.saveProduct(finalProduct)
            if (saveSuccess) {
                if (oldProduct.code != finalProduct.code) {
                    android.util.Log.d("ProductSync", "Código alterado de ${oldProduct.code} para ${finalProduct.code}. Excluindo antigo.")
                    val deleteSuccess = com.example.data.FirebaseService.deleteProduct(oldProduct.code)
                    if (!deleteSuccess) {
                        android.util.Log.e("ProductSync", "Erro ao excluir documento antigo: ${oldProduct.code}")
                    }
                }
                
                android.util.Log.d("ProductSync", "Atualizando Room: ${finalProduct.code}")
                repository.updateProduct(finalProduct)
                
                val type = when {
                    oldProduct.code != finalProduct.code && oldProduct.name != finalProduct.name -> "INFO_CHANGED"
                    oldProduct.code != finalProduct.code -> "CODE_CHANGED"
                    oldProduct.name != finalProduct.name -> "NAME_CHANGED"
                    else -> "INFO_CHANGED"
                }
                
                android.util.Log.d("ProductSync", "Publicando evento: $type")
                com.example.data.FirebaseService.publishProductEvent(type, finalProduct.name, oldProduct.name, finalProduct.code)
                _syncMessage.emit("Produto atualizado na nuvem!")
                return true
            } else {
                android.util.Log.e("ProductSync", "Save Firestore falhou para edição: ${finalProduct.code}")
                _syncMessage.emit("Erro ao atualizar produto na nuvem.")
                return false
            }
        } else {
            repository.updateProduct(finalProduct)
            _syncMessage.emit("Atualizado apenas localmente")
            return true
        }
    }"""

import re
content = re.sub(r'suspend fun addProductSuspend.*?_newProductsCount\.value \+= 1\s*\}', add_replacement, content, flags=re.DOTALL)
content = re.sub(r'suspend fun updateProductSuspend.*?_syncMessage\.emit\("Produto atualizado na nuvem!"\)\s*\}\s*\}', update_replacement, content, flags=re.DOTALL)

open("app/src/main/java/com/example/ui/MainViewModel.kt", "w").write(content)
print("Success")
