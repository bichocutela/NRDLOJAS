import re

with open('app/src/main/java/com/example/data/ProductDao.kt', 'r') as f:
    content = f.read()

if 'import androidx.room.Delete' not in content:
    content = content.replace('import androidx.room.Update', 'import androidx.room.Update\nimport androidx.room.Delete')

if 'fun deleteProduct' not in content:
    content = content.replace('suspend fun insertProduct(product: Product)', 
                              '@Delete\n    suspend fun deleteProduct(product: Product)\n\n    @Delete\n    suspend fun deleteProducts(products: List<Product>)\n\n    @Insert(onConflict = OnConflictStrategy.REPLACE)\n    suspend fun insertProduct(product: Product)')

with open('app/src/main/java/com/example/data/ProductDao.kt', 'w') as f:
    f.write(content)
print("Patched ProductDao")

with open('app/src/main/java/com/example/data/ProductRepository.kt', 'r') as f:
    content = f.read()

if 'suspend fun deleteProduct' not in content:
    content = content.replace('suspend fun insertProduct(product: Product) {', 
                              'suspend fun deleteProduct(product: Product) {\n        dao.deleteProduct(product)\n    }\n\n    suspend fun deleteProducts(products: List<Product>) {\n        dao.deleteProducts(products)\n    }\n\n    suspend fun insertProduct(product: Product) {')

with open('app/src/main/java/com/example/data/ProductRepository.kt', 'w') as f:
    f.write(content)
print("Patched ProductRepository")

