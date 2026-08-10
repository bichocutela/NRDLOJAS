import sys
content = open("app/src/main/java/com/example/data/FirebaseService.kt").read()

target = """    suspend fun saveProduct(product: com.example.data.Product) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("products").document(product.code)
                .set(mapOf(
                    "code" to product.code,
                    "name" to product.name,
                    "searchName" to product.searchName,
                    "category" to product.category,
                    "unit" to product.unit,
                    "imageUrl" to product.imageUrl,
                    "searchCount" to product.searchCount,
                    "timestamp" to System.currentTimeMillis()
                )).await()
                
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error saving product", e)
        }
    }
        
    suspend fun deleteProduct(code: String) {
        if (!isFirebaseConfigured()) return
        try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("products").document(code).delete().await()
        } catch (e: Exception) {
            Log.e("FirebaseService", "Error deleting product", e)
        }
    }"""

import re
# Find where it starts
match = re.search(r'suspend fun saveProduct.*?Log.e\("FirebaseService", "Error deleting product", e\)\s*\}', content, re.DOTALL)
if match:
    replacement = """    suspend fun saveProduct(product: com.example.data.Product): Boolean {
        if (!isFirebaseConfigured()) return false
        return try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("products").document(product.code)
                .set(mapOf(
                    "code" to product.code,
                    "name" to product.name,
                    "searchName" to product.searchName,
                    "category" to product.category,
                    "unit" to product.unit,
                    "imageUrl" to product.imageUrl,
                    "searchCount" to product.searchCount,
                    "timestamp" to System.currentTimeMillis()
                )).await()
            Log.d("ProductSync", "Produto salvo no Firestore: ${product.code}")
            true
        } catch (e: Exception) {
            Log.e("ProductSync", "Erro ao salvar no Firestore: ${product.code}", e)
            false
        }
    }
        
    suspend fun deleteProduct(code: String): Boolean {
        if (!isFirebaseConfigured()) return false
        return try {
            val firestore = FirebaseFirestore.getInstance()
            firestore.collection("products").document(code).delete().await()
            Log.d("ProductSync", "Produto excluído do Firestore: $code")
            true
        } catch (e: Exception) {
            Log.e("ProductSync", "Erro ao excluir do Firestore: $code", e)
            false
        }
    }"""
    
    new_content = content.replace(match.group(0), replacement)
    open("app/src/main/java/com/example/data/FirebaseService.kt", "w").write(new_content)
    print("Success")
else:
    print("Not found")

